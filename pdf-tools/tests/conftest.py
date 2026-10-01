"""Shared test helpers. Tests build their own PDFs, so no real documents are ever committed."""

from collections.abc import Callable
from pathlib import Path

import pytest
from pypdf import PdfWriter


@pytest.fixture
def make_pdf(tmp_path: Path) -> Callable[[int], Path]:
    """Return a function that writes a blank PDF with the given number of pages.

    Each page gets a different width (101, 102, 103...) so tests can check page order.
    """

    def _make(pages: int, name: str = "sample.pdf") -> Path:
        writer = PdfWriter()
        for i in range(pages):
            writer.add_blank_page(width=101 + i, height=200)
        path = tmp_path / name
        with path.open("wb") as f:
            writer.write(f)
        return path

    return _make
