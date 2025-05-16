import json

import google.generativeai as genai
from app.core.config import settings


class LLMService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.llm = genai.GenerativeModel(settings.GEMINI_MODEL_ID)

    def generate_answer(self, query: str, chunks: list[str]) -> str:
        """
        Generate an answer based on provided document chunks and a user query.

        Args:
            query (str): The question to be answered.
            chunks (list[str]): List of document text excerpts.

        Returns:
            str: The generated answer text.
        """
        context = "\n\n".join(chunks)
        prompt = f"""
Use the excerpts from the document below to answer the user's question. Always provide the answer in the same language as the question.

Document excerpts:
------------------
{context}
------------------

Question:
{query}

Answer concisely and accurately, based only on the information provided in the excerpts above.
"""

        response = self.llm.generate_content(prompt)
        return response.text

    def answer_validator(self, question: str, answer: str) -> bool:
        """
        Validate whether the provided answer correctly responds to the question.

        Args:
            question (str): The original question.
            answer (str): The answer to validate.

        Returns:
            bool: True if the answer is valid, False otherwise.
        """
        prompt = f"""
Assess whether the provided answer correctly and sufficiently responds to the question.
Check if the answer is in the same language as the question. 
Only consider the question and the answer — do not assume any external context.

Return your output as a valid JSON object in the following format:
{{
  "is_valid": true or false
}}

Question:
{question}

Answer:
{answer}
"""
        response = self.llm.generate_content(prompt)
        # Clean the response from possible markdown formatting or code fences
        cleaned_response = response.text.strip().lstrip('```json').rstrip('```').strip()

        try:
            parsed = json.loads(cleaned_response)
            return parsed.get("is_valid", False)
        except (json.JSONDecodeError, TypeError):
            # Fallback to False if parsing fails
            return False
