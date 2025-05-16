from fastapi import FastAPI, HTTPException
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from pydantic import BaseModel
from pathlib import Path
import tempfile
import os

app = FastAPI()

INDEX_PATH = "app/faiss_index"
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

if Path(f"{INDEX_PATH}/index.faiss").exists():
    vectorstore = FAISS.load_local(INDEX_PATH, embedding_model)
else:
    vectorstore = None

class UploadInput(BaseModel):
    text: str
    chunk_size: int
    chunk_overlap: int

@app.post("/upload/")
async def upload_document(data: UploadInput):
    global vectorstore

    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as temp_file:
        temp_file.write(data.text.encode('utf-8'))
        filepath = temp_file.name

    try:
        loader = TextLoader(filepath, encoding="utf-8")
        docs = loader.load()

        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=data.chunk_size,
            chunk_overlap=data.chunk_overlap
        )
        chunks = splitter.split_documents(docs)

        chunk_offset = vectorstore.index.ntotal if vectorstore else 0

        for i, chunk in enumerate(chunks):
            chunk.metadata["chunk_number"] = chunk_offset + i

        if vectorstore:
            vectorstore.add_documents(chunks)
        else:
            vectorstore = FAISS.from_documents(chunks, embedding_model)

        vectorstore.save_local(INDEX_PATH)
        return {
            "status": "Document successfully indexed",
            "total_chunks": len(chunks)
        }
    
    finally:
        os.unlink(filepath)

@app.get("/query/")
def query(q: str):
    global vectorstore

    if not vectorstore:
        raise HTTPException(status_code=404, detail="No document has been indexed yet")

    retriever = vectorstore.as_retriever()
    relevant_docs = retriever.get_relevant_documents(q)

    retrieved_chunks = [
        {
            "chunk_number": doc.metadata.get("chunk_number", -1),
            "content": doc.page_content
        }
        for doc in relevant_docs
    ]

    return {
        "retrieved_chunks": retrieved_chunks
    }