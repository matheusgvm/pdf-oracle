# Project PDF Oracle

## Description
This system lets users upload PDF documents and ask questions about their content. It extracts text (using OCR if needed), breaks it into chunks, embeds them for semantic search, and stores these embeddings for fast retrieval. A large language model (LLM) then answers user questions accurately based on the uploaded documents. The project highlights retrieval-augmented generation (RAG) and integrates all components into a working solution.

## GitHub Repository
`https://github.com/matheusgvm/pdf-oracle`

## Setup and Running Instructions
1) Copy the example environment file and customize it with your AWS credentials with S3 access and Gemini API key.

        cp .env.example .env

2) Run the application with Docker Compose:

         bash docker-compose up --build

3) Ensure ports configured in docker-compose.yml are available

## Example Requests and Expected Responses
### Example Request — Upload PDF Documents

```bash
curl -X POST "http://localhost:8001/v1/documents/" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@/path/to/document1.pdf" \
  -F "files=@/path/to/document2.pdf"
```
### Expected Response
```json
{
  "message": "Documents processed successfully",
  "documents_indexed": 2,
  "total_chunks": 50
}
```

### Example Request — Ask a Question

```bash
curl -X POST "http://localhost:8001/v1/question" \
  -H "Content-Type: application/json" \
  -d '{"question": "How often should I replace the water filter?"}'
```

### Expected Response
```json
{
  "answer": "You should replace the water filter every 6 months or after filtering 2,000 liters, whichever comes first."
}
```