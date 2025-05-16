from app.services.llm_service import LLMService
from app.services.rag_service import RAGService


class InferencePipeline:
    """
    Pipeline to generate an answer to a question based on retrieved document chunks.
    """

    def generate_question_answer(self, question: str) -> str:
        """
        Generate an answer for the input question using retrieval-augmented generation (RAG).

        Args:
            question (str): The input question string.

        Returns:
            str: The generated answer or an appropriate fallback message.
        """
        rag_service = RAGService()
        chunks_response = rag_service.retrieve_chunks(question)

        if not chunks_response:
            return "No relevant information found in the indexed documents."

        chunks = chunks_response.get("retrieved_chunks", [])
        if not chunks:
            return "No relevant information found in the indexed documents."

        retrieved_chunks_text = [chunk["content"].replace("\n", " ") for chunk in chunks]

        llm_service = LLMService()
        answer = llm_service.generate_answer(question, retrieved_chunks_text)
        is_answer_valid = llm_service.answer_validator(question, answer)

        if is_answer_valid:
            return answer
        else:
            return "Invalid answer. Please try again."
