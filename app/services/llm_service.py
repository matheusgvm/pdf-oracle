import google.generativeai as genai
from app.core.config import settings

class LLMService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.llm = genai.GenerativeModel(settings.GEMINI_MODEL_ID)

    def generate_answer(self, query: str, chunks) -> str:
        context = "\n\n".join(chunks)
        prompt = f"""
        Use the excerpts from the document below to answer the user's question.

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
        prompt = f"""
        Assess whether the provided answer correctly and sufficiently responds to the question. 
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
        return response.text