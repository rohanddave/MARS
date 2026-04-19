from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader


class PDFTextReader:
    def read(self, path: str | Path) -> str:
        pdf_path = Path(path)
        reader = PdfReader(pdf_path)
        pages: list[str] = []

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                pages.append(f"\n\n[Page {page_number}]\n{text.strip()}")

        return "\n".join(pages).strip()
