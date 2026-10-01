"""Split a PDF into smaller PDFs of a fixed number of pages."""

from pathlib import Path

from pypdf import PdfReader, PdfWriter


def split_pdf(input_path: Path, output_dir: Path, every: int) -> list[Path]:
    """Split ``input_path`` into parts of ``every`` pages each, written to ``output_dir``.

    The last part holds whatever pages are left over. Returns the created files in page order.
    Raises ValueError if ``every`` is less than 1 or the PDF has no pages.
    """
    if every < 1:
        raise ValueError(f"'every' must be 1 or more, got {every}")

    reader = PdfReader(input_path)
    total_pages = len(reader.pages)
    if total_pages == 0:
        raise ValueError(f"{input_path.name} has no pages")

    output_dir.mkdir(parents=True, exist_ok=True)

    # Pad page numbers to the same width (001, 010, 100) so files sort in page order.
    width = len(str(total_pages))
    created: list[Path] = []

    for start in range(0, total_pages, every):
        end = min(start + every, total_pages)
        writer = PdfWriter()
        for page_index in range(start, end):
            writer.add_page(reader.pages[page_index])

        # Page indexes start at 0; people count pages from 1.
        name = f"{input_path.stem}_pages_{start + 1:0{width}d}-{end:0{width}d}.pdf"
        output_path = output_dir / name
        with output_path.open("wb") as output_file:
            writer.write(output_file)
        created.append(output_path)

    return created
