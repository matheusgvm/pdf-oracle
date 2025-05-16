from fastapi import FastAPI
from app.api.endpoints import upload_document_endpoint
from app.api.endpoints import question_endpoint
app = FastAPI(
    title="PDF Oracle",
    version="1.0.0",
    description="API for answering questions based on the content of an uploaded PDF",
)

app.include_router(upload_document_endpoint.router, prefix="/v1/documents", tags=["Upload"])
app.include_router(question_endpoint.router, prefix="/v1/question", tags=["Question"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)