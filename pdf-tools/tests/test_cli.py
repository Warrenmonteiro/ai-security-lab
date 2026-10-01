from typer.testing import CliRunner

from pdf_tools.cli import app

runner = CliRunner()


def test_split_command_creates_files(make_pdf, tmp_path):
    out = tmp_path / "parts"

    result = runner.invoke(app, ["split", str(make_pdf(12)), "--every", "5", "--out", str(out)])

    assert result.exit_code == 0
    assert "Created 3 file(s)" in result.output
    assert len(list(out.glob("*.pdf"))) == 3


def test_missing_file_is_rejected(tmp_path):
    result = runner.invoke(app, ["split", str(tmp_path / "nope.pdf")])

    assert result.exit_code == 2  # Typer's code for bad arguments


def test_every_zero_is_rejected(make_pdf):
    result = runner.invoke(app, ["split", str(make_pdf(5)), "--every", "0"])

    assert result.exit_code == 2


def test_file_that_is_not_a_pdf_gives_clear_error(tmp_path):
    fake = tmp_path / "notes.pdf"
    fake.write_text("this is not a PDF")

    result = runner.invoke(app, ["split", str(fake), "--out", str(tmp_path / "parts")])

    assert result.exit_code == 1
    assert "Error:" in result.output
