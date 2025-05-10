from fastapi import FastAPI
from app.api.endpoints import upload, inference

app = FastAPI(
    title="PDF Oracle",
    version="1.0.0",
    description="API for answering questions based on the content of an uploaded PDF",
)

# Incluir rotas
app.include_router(upload.router, prefix="/v1/upload", tags=["Upload"])
app.include_router(inference.router, prefix="/v1/inference", tags=["Inference"])