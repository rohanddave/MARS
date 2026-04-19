from __future__ import annotations

import logging
from pathlib import Path

from pypdf import PdfReader

logger = logging.getLogger(__name__)


class PDFTextReader:
    def read(self, path: str | Path) -> str:
        pdf_path = Path(path)
        logger.info("Reading PDF path=%s", pdf_path)
        reader = PdfReader(pdf_path)
        pages: list[str] = []

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                pages.append(f"\n\n[Page {page_number}]\n{text.strip()}")

        result = "\n".join(pages).strip()
        logger.info("Finished reading PDF path=%s pages=%s extracted_chars=%s", pdf_path, len(reader.pages), len(result))
        return result
