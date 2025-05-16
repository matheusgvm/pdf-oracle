from app.services.llm_service import LLMService
from app.services.rag_service import RAGService

class InferencePipeline:
    def generate_question_answer(self, question: str) -> str:

        # Getting chunks
        rag_service = RAGService()
        chunks = rag_service.retrieve_chunks(question)

        if not chunks:
            return "No relevant information found in the indexed documents."

        # Generating answer
        llm_service = LLMService()
        answer = llm_service.generate_answer(question, chunks)
        is_answer_valid = llm_service.answer_validator(question, answer)

        if is_answer_valid:
            return answer
        else:
            return "Invalided answer. Please try again."
