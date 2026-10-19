from fastapi.testclient import TestClient

from pdf_tools import api
from pdf_tools.api import app

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_upload_is_valid_pdf(make_pdf):
    pdf_bytes = make_pdf(5).read_bytes()
    response = client.post(
        "/pdf/page-count", files={"file": ("sample.pdf", pdf_bytes, "application/pdf")}
    )
    assert response.status_code == 200
    assert response.json() == {"pages": 5}


def test_not_a_pdf():
    response = client.post(
        "/pdf/page-count", files={"file": ("sample.doc", b"This is not a pdf", "text/plain")}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "File is not a PDF"}


def test_no_file_provided():
    response = client.post("/pdf/page-count")
    assert response.status_code == 422


def test_empty_file():
    response = client.post("/pdf/page-count", files={"file": ("sample.doc", b"", "text/plain")})
    assert response.status_code == 400


def test_oversized_file(make_pdf, monkeypatch):
    pdf_bytes = make_pdf(5).read_bytes()
    monkeypatch.setattr(api, "MAX_UPLOAD_BYTES", 20)
    response = client.post(
        "/pdf/page-count", files={"file": ("sample.pdf", pdf_bytes, "application/pdf")}
    )
    assert response.status_code == 413
    assert response.json() == {"detail": "Max File Size is 20MB"}
