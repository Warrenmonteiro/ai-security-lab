import io

from fastapi import FastAPI, HTTPException, UploadFile
from pydantic import BaseModel
from pypdf import PdfReader
from pypdf.errors import PdfReadError

MAX_UPLOAD_BYTES = 20 * 1024 * 1024


class PageCount(BaseModel):
    pages: int


app = FastAPI()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/pdf/page-count")
async def page_count(file: UploadFile) -> PageCount:

    try:
        data = await file.read()
        if len(data) > MAX_UPLOAD_BYTES:
            raise HTTPException(status_code=413, detail="Max File Size is 20MB")
        reader = PdfReader(io.BytesIO(data))
        return PageCount(pages=len(reader.pages))
    except PdfReadError as error:
        raise HTTPException(status_code=400, detail="File is not a PDF") from error
