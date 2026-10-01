# pdf-tools

A small command-line tool for splitting PDFs into parts of a fixed number of pages.

It started as a one-off script I wrote for a work task. I rebuilt it as a tested tool. The original
only ever split a hard-coded range of pages, ran as soon as it was imported, and dropped pages that
failed to copy instead of stopping. The tests in `tests/` now check that every page ends up in the
output, in order, and that bad input fails with a clear error.

## Install

Requires [uv](https://docs.astral.sh/uv/).

```bash
cd pdf-tools
uv sync
```

## Usage

```bash
# Split into parts of 10 pages (the default) in the current folder
uv run pdf-tools split report.pdf

# Split into parts of 25 pages, written to ./parts
uv run pdf-tools split report.pdf --every 25 --out ./parts
```

A 23-page `report.pdf` split every 10 pages gives:

```
report_pages_01-10.pdf
report_pages_11-20.pdf
report_pages_21-23.pdf
```

## Development

```bash
uv run pytest             # tests
uv run ruff check .       # lint
uv run ruff format .      # format
```

CI runs all three on every push that touches this folder.
