"""Command-line interface: `pdf-tools split input.pdf --every 10 --out ./parts`."""

from pathlib import Path
from typing import Annotated

import typer
from pypdf.errors import PdfReadError

from pdf_tools.split import split_pdf

app = typer.Typer(help="Small, tested PDF utilities.", no_args_is_help=True)


@app.callback()
def main() -> None:
    """Small, tested PDF utilities."""
    # A callback keeps `split` as a named subcommand, so more commands can be added later.


@app.command()
def split(
    input_pdf: Annotated[
        Path,
        typer.Argument(exists=True, dir_okay=False, readable=True, help="The PDF to split."),
    ],
    every: Annotated[int, typer.Option("--every", "-n", min=1, help="Pages per part.")] = 10,
    out: Annotated[
        Path, typer.Option("--out", "-o", file_okay=False, help="Folder for the parts.")
    ] = Path("."),
) -> None:
    """Split a PDF into parts of EVERY pages."""
    try:
        files = split_pdf(input_pdf, out, every)
    except (PdfReadError, ValueError) as error:
        typer.echo(f"Error: {error}", err=True)
        raise typer.Exit(code=1) from error

    for path in files:
        typer.echo(path)
    typer.echo(f"Created {len(files)} file(s) in {out}")
