from __future__ import annotations

import hashlib
import json
import logging
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from app.embedder import OpenAIEmbedder
from app.file_reader import PDFTextReader
from app.vector_store import EmbeddingRecord, PineconeVectorStore

logger = logging.getLogger(__name__)


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
    skipped: bool = False


@dataclass(frozen=True)
class IngestionResult:
    files: list[IngestedFile]
    chunk_count: int
    skipped_file_count: int = 0


@dataclass
class IngestionManifest:
    files: dict[str, dict[str, Any]] = field(default_factory=dict)


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
        manifest_path: str | Path | None = None,
        chunk_cache_dir: str | Path | None = None,
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
        self.manifest_path = Path(manifest_path) if manifest_path is not None else self.data_dir / ".ingestion_manifest.json"
        self.chunk_cache_dir = Path(chunk_cache_dir) if chunk_cache_dir is not None else self.data_dir / ".embedding_cache"

    async def ingest(self) -> IngestionResult:
        logger.info(
            "Starting ingestion data_dir=%s chunk_size_chars=%s chunk_overlap_chars=%s batch_size=%s",
            self.data_dir,
            self.chunk_size_chars,
            self.chunk_overlap_chars,
            self.batch_size,
        )
        if not self.data_dir.exists():
            raise FileNotFoundError(f"Data directory does not exist: {self.data_dir}")
        if not self.data_dir.is_dir():
            raise NotADirectoryError(f"Data path is not a directory: {self.data_dir}")

        ingested_files: list[IngestedFile] = []
        total_chunks = 0
        skipped_file_count = 0

        files = self._iter_supported_files()
        manifest = self._load_manifest()
        logger.info("Found supported files count=%s", len(files))
        ingestion_started_at = time.perf_counter()
        for file_number, file_path in enumerate(files, start=1):
            file_started_at = time.perf_counter()
            logger.info("Ingesting file %s/%s path=%s", file_number, len(files), file_path)
            fingerprint = _file_fingerprint(file_path)
            manifest_key = self._manifest_key(file_path)
            manifest_entry = manifest.files.get(manifest_key)
            if manifest_entry and manifest_entry.get("fingerprint") == fingerprint:
                chunk_count = _optional_int(manifest_entry.get("chunk_count")) or 0
                skipped_file_count += 1
                logger.info(
                    "Skipping already embedded file %s/%s path=%s chunks=%s fingerprint=%s",
                    file_number,
                    len(files),
                    file_path,
                    chunk_count,
                    fingerprint,
                )
                ingested_files.append(IngestedFile(path=file_path, chunk_count=chunk_count, skipped=True))
                continue

            text = _normalize_text(self._read_file(file_path))
            if not text:
                logger.warning("No text extracted from file path=%s", file_path)
                ingested_files.append(IngestedFile(path=file_path, chunk_count=0))
                continue

            chunks = self._chunk_text(text)
            logger.info("Chunked file path=%s text_chars=%s chunks=%s", file_path, len(text), len(chunks))
            file_records: list[EmbeddingRecord] = []
            for chunk_number, chunk in enumerate(chunks, start=1):
                cache_key = self._chunk_cache_key(chunk.text)
                logger.info(
                    "Embedding chunk file=%s/%s path=%s chunk=%s/%s chunk_chars=%s elapsed_seconds=%.1f",
                    file_number,
                    len(files),
                    file_path,
                    chunk_number,
                    len(chunks),
                    len(chunk.text),
                    time.perf_counter() - ingestion_started_at,
                )
                embedding = self._load_cached_embedding(cache_key)
                if embedding is None:
                    embedding = await self.embedder.embed(chunk.text)
                    self._save_cached_embedding(cache_key, embedding)
                else:
                    logger.info(
                        "Using cached embedding file=%s/%s path=%s chunk=%s/%s vector_dimensions=%s",
                        file_number,
                        len(files),
                        file_path,
                        chunk_number,
                        len(chunks),
                        len(embedding),
                    )
                logger.info(
                    "Embedded chunk file=%s/%s path=%s chunk=%s/%s vector_dimensions=%s",
                    file_number,
                    len(files),
                    file_path,
                    chunk_number,
                    len(chunks),
                    len(embedding),
                )
                file_records.append(
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

            self._upsert_file_records(file_path, file_records)
            manifest.files[manifest_key] = {
                "fingerprint": fingerprint,
                "chunk_count": len(chunks),
                "embedded_at_unix": time.time(),
                "chunk_size_chars": self.chunk_size_chars,
                "chunk_overlap_chars": self.chunk_overlap_chars,
            }
            self._save_manifest(manifest)
            logger.info("Marked file as embedded path=%s manifest=%s", file_path, self.manifest_path)

            ingested_files.append(IngestedFile(path=file_path, chunk_count=len(chunks)))
            logger.info(
                "Finished ingesting file %s/%s path=%s chunks=%s file_elapsed_seconds=%.1f total_elapsed_seconds=%.1f",
                file_number,
                len(files),
                file_path,
                len(chunks),
                time.perf_counter() - file_started_at,
                time.perf_counter() - ingestion_started_at,
            )

        logger.info(
            "Ingestion complete files=%s chunks=%s skipped_files=%s",
            len(ingested_files),
            total_chunks,
            skipped_file_count,
        )
        return IngestionResult(files=ingested_files, chunk_count=total_chunks, skipped_file_count=skipped_file_count)

    def _upsert_file_records(self, file_path: Path, records: list[EmbeddingRecord]) -> None:
        for batch_start in range(0, len(records), self.batch_size):
            batch = records[batch_start : batch_start + self.batch_size]
            logger.info(
                "Upserting file batch path=%s batch=%s-%s/%s",
                file_path,
                batch_start + 1,
                batch_start + len(batch),
                len(records),
            )
            self.vector_store.insert_embeddings(batch)

    def _iter_supported_files(self) -> list[Path]:
        paths = [*self.data_dir.rglob("*.pdf"), *self.data_dir.rglob("*.txt")]
        return sorted(paths)

    def _read_file(self, file_path: Path) -> str:
        if file_path.suffix.lower() == ".pdf":
            return self.pdf_reader.read(file_path)
        return file_path.read_text(encoding="utf-8")

    def _load_manifest(self) -> IngestionManifest:
        if not self.manifest_path.exists():
            logger.info("No ingestion manifest found path=%s", self.manifest_path)
            return IngestionManifest()

        try:
            payload = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            logger.warning("Could not parse ingestion manifest path=%s; rebuilding it", self.manifest_path)
            return IngestionManifest()

        files = payload.get("files") if isinstance(payload, dict) else None
        if not isinstance(files, dict):
            logger.warning("Invalid ingestion manifest shape path=%s; rebuilding it", self.manifest_path)
            return IngestionManifest()
        logger.info("Loaded ingestion manifest path=%s tracked_files=%s", self.manifest_path, len(files))
        return IngestionManifest(files=files)

    def _save_manifest(self, manifest: IngestionManifest) -> None:
        self.manifest_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = self.manifest_path.with_suffix(f"{self.manifest_path.suffix}.tmp")
        payload = {"files": manifest.files}
        tmp_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        tmp_path.replace(self.manifest_path)

    def _manifest_key(self, file_path: Path) -> str:
        try:
            return file_path.relative_to(self.data_dir).as_posix()
        except ValueError:
            return file_path.as_posix()

    def _chunk_cache_key(self, text: str) -> str:
        settings = self.embedder.llm_client.settings
        raw_key = "\n".join(
            [
                settings.openai_embedding_model,
                str(settings.openai_embedding_dimensions),
                hashlib.sha256(text.encode("utf-8")).hexdigest(),
            ]
        )
        return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()

    def _chunk_cache_path(self, cache_key: str) -> Path:
        return self.chunk_cache_dir / f"{cache_key}.json"

    def _load_cached_embedding(self, cache_key: str) -> list[float] | None:
        cache_path = self._chunk_cache_path(cache_key)
        if not cache_path.exists():
            return None

        try:
            payload = json.loads(cache_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            logger.warning("Ignoring invalid embedding cache file path=%s", cache_path)
            return None

        embedding = payload.get("embedding") if isinstance(payload, dict) else None
        if not isinstance(embedding, list):
            logger.warning("Ignoring embedding cache with missing vector path=%s", cache_path)
            return None
        if not all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in embedding):
            logger.warning("Ignoring embedding cache with non-numeric vector path=%s", cache_path)
            return None

        logger.info("Loaded cached embedding cache_key=%s vector_dimensions=%s", cache_key, len(embedding))
        return [float(value) for value in embedding]

    def _save_cached_embedding(self, cache_key: str, embedding: list[float]) -> None:
        self.chunk_cache_dir.mkdir(parents=True, exist_ok=True)
        cache_path = self._chunk_cache_path(cache_key)
        tmp_path = cache_path.with_suffix(".json.tmp")
        settings = self.embedder.llm_client.settings
        payload = {
            "embedding_model": settings.openai_embedding_model,
            "embedding_dimensions": settings.openai_embedding_dimensions,
            "embedding": embedding,
        }
        tmp_path.write_text(json.dumps(payload), encoding="utf-8")
        tmp_path.replace(cache_path)
        logger.info("Saved cached embedding cache_key=%s vector_dimensions=%s", cache_key, len(embedding))

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


def _file_fingerprint(file_path: Path) -> str:
    digest = hashlib.sha256()
    with file_path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _optional_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    return None
