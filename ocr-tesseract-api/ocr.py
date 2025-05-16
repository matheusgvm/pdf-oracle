from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pdf2image import convert_from_bytes
import pytesseract

app = FastAPI()

@app.post("/ocr/")
async def ocr_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        return JSONResponse(status_code=400, content={"error": "Arquivo precisa ser PDF"})

    contents = await file.read()
    try:
        pages = convert_from_bytes(contents)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": f"Erro ao processar PDF: {e}"})

    texts = []
    for i, page in enumerate(pages):
        text = pytesseract.image_to_string(page, lang="por")
        texts.append({"page": i + 1, "text": text})

    return {"pages": texts}
