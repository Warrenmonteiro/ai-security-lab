from pathlib import Path

import pytest
from pypdf import PdfReader

from pdf_tools.split import split_pdf


def page_count(path: Path) -> int:
    return len(PdfReader(path).pages)


def page_widths(path: Path) -> list[int]:
    return [round(float(page.mediabox.width)) for page in PdfReader(path).pages]


def test_splits_into_parts_with_leftover(make_pdf, tmp_path):
    files = split_pdf(make_pdf(25), tmp_path / "out", every=10)

    assert [page_count(f) for f in files] == [10, 10, 5]


def test_covers_every_page_in_order(make_pdf, tmp_path):
    files = split_pdf(make_pdf(25), tmp_path / "out", every=10)

    widths = [w for f in files for w in page_widths(f)]
    assert widths == list(range(101, 126))  # pages 1-25, nothing skipped or reordered


def test_short_pdf_gives_one_file(make_pdf, tmp_path):
    files = split_pdf(make_pdf(3), tmp_path / "out", every=10)

    assert len(files) == 1
    assert page_count(files[0]) == 3


def test_exact_multiple_has_no_empty_part(make_pdf, tmp_path):
    files = split_pdf(make_pdf(20), tmp_path / "out", every=10)

    assert [page_count(f) for f in files] == [10, 10]


def test_file_names_use_page_numbers_and_sort_in_order(make_pdf, tmp_path):
    files = split_pdf(make_pdf(25), tmp_path / "out", every=10)

    assert [f.name for f in files] == [
        "sample_pages_01-10.pdf",
        "sample_pages_11-20.pdf",
        "sample_pages_21-25.pdf",
    ]
    assert sorted(files) == files


def test_creates_missing_output_folder(make_pdf, tmp_path):
    out = tmp_path / "does" / "not" / "exist"

    split_pdf(make_pdf(5), out, every=2)

    assert out.is_dir()


@pytest.mark.parametrize("every", [0, -1])
def test_rejects_every_below_one(make_pdf, tmp_path, every):
    with pytest.raises(ValueError, match="1 or more"):
        split_pdf(make_pdf(5), tmp_path / "out", every=every)
