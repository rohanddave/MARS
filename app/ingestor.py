from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

from app.embedder import OpenAIEmbedder
from app.file_reader import PDFTextReader
from app.vector_store import EmbeddingRecord, PineconeVectorStore


@dataclass(frozen=True)
class TextChunk:
    text: str
    chunk_index: int
    char_start: int
    char_end: int


@dataclass(frozen=True)
class IngestedFile:
    path: Path
    chunk_count: int


@dataclass(frozen=True)
class IngestionResult:
    files: list[IngestedFile]
    chunk_count: int


class ResearchPaperIngestor:
    def __init__(
        self,
        embedder: OpenAIEmbedder,
        vector_store: PineconeVectorStore,
        data_dir: str | Path = "data",
        chunk_size_chars: int = 4_000,
        chunk_overlap_chars: int = 400,
        batch_size: int = 25,
        pdf_reader: PDFTextReader | None = None,
    ) -> None:
        if chunk_size_chars <= 0:
            raise ValueError("chunk_size_chars must be greater than 0")
        if chunk_overlap_chars < 0:
            raise ValueError("chunk_overlap_chars must be greater than or equal to 0")
        if chunk_overlap_chars >= chunk_size_chars:
            raise ValueError("chunk_overlap_chars must be smaller than chunk_size_chars")
        if batch_size <= 0:
            raise ValueError("batch_size must be greater than 0")

        self.embedder = embedder
        self.vector_store = vector_store
        self.data_dir = Path(data_dir)
        self.chunk_size_chars = chunk_size_chars
        self.chunk_overlap_chars = chunk_overlap_chars
        self.batch_size = batch_size
        self.pdf_reader = pdf_reader or PDFTextReader()

    async def ingest(self) -> IngestionResult:
        if not self.data_dir.exists():
            raise FileNotFoundError(f"Data directory does not exist: {self.data_dir}")
        if not self.data_dir.is_dir():
            raise NotADirectoryError(f"Data path is not a directory: {self.data_dir}")

        ingested_files: list[IngestedFile] = []
        pending_records: list[EmbeddingRecord] = []
        total_chunks = 0

        for file_path in self._iter_supported_files():
            text = _normalize_text(self._read_file(file_path))
            if not text:
                ingested_files.append(IngestedFile(path=file_path, chunk_count=0))
                continue

            chunks = self._chunk_text(text)
            for chunk in chunks:
                embedding = await self.embedder.embed(chunk.text)
                pending_records.append(
                    EmbeddingRecord(
                        id=_record_id(file_path, chunk),
                        values=embedding,
                        metadata={
                            "source": str(file_path),
                            "filename": file_path.name,
                            "file_type": file_path.suffix.lower().lstrip("."),
                            "chunk_index": chunk.chunk_index,
                            "char_start": chunk.char_start,
                            "char_end": chunk.char_end,
                            "text": chunk.text,
                        },
                    )
                )
                total_chunks += 1

                if len(pending_records) >= self.batch_size:
                    self.vector_store.insert_embeddings(pending_records)
                    pending_records = []

            ingested_files.append(IngestedFile(path=file_path, chunk_count=len(chunks)))

        if pending_records:
            self.vector_store.insert_embeddings(pending_records)

        return IngestionResult(files=ingested_files, chunk_count=total_chunks)

    def _iter_supported_files(self) -> list[Path]:
        paths = [*self.data_dir.rglob("*.pdf"), *self.data_dir.rglob("*.txt")]
        return sorted(paths)

    def _read_file(self, file_path: Path) -> str:
        if file_path.suffix.lower() == ".pdf":
            return self.pdf_reader.read(file_path)
        return file_path.read_text(encoding="utf-8")

    def _chunk_text(self, text: str) -> list[TextChunk]:
        chunks: list[TextChunk] = []
        start = 0

        while start < len(text):
            end = min(start + self.chunk_size_chars, len(text))
            if end < len(text):
                boundary = _best_chunk_boundary(text, start, end)
                if boundary > start:
                    end = boundary

            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append(
                    TextChunk(
                        text=chunk_text,
                        chunk_index=len(chunks),
                        char_start=start,
                        char_end=end,
                    )
                )

            if end >= len(text):
                break
            start = max(end - self.chunk_overlap_chars, start + 1)

        return chunks


def _normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _best_chunk_boundary(text: str, start: int, end: int) -> int:
    paragraph_break = text.rfind("\n\n", start, end)
    if paragraph_break > start:
        return paragraph_break

    sentence_breaks = [text.rfind(marker, start, end) for marker in (". ", "? ", "! ")]
    sentence_break = max(sentence_breaks)
    if sentence_break > start:
        return sentence_break + 1

    whitespace = text.rfind(" ", start, end)
    if whitespace > start:
        return whitespace

    return end


def _record_id(file_path: Path, chunk: TextChunk) -> str:
    raw_id = f"{file_path.as_posix()}:{chunk.chunk_index}:{chunk.text}".encode("utf-8")
    digest = hashlib.sha256(raw_id).hexdigest()[:24]
    return f"{file_path.stem}-{chunk.chunk_index}-{digest}"
