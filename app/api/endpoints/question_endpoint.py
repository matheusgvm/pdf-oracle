from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.pipelines.inference_pipeline import InferencePipeline

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str

@router.post("/", summary="Answer a question using indexed documents")
async def answer_question(request: QuestionRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    #try:
    answer = InferencePipeline().generate_question_answer(question)
    return AnswerResponse(answer=answer)
    """
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating answer: {str(e)}")
    """