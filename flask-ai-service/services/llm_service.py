# llm_service.py
# Handles communication with the LLM (OpenAI API + fallback)

from config import config


class LLMService:

    def generate_response(self, question: str, context: str) -> str:
        """
        RAG Generation step:
        1. Build prompt
        2. Call LLM (OpenAI)
        3. Fallback if API fails
        """

        prompt = self._build_prompt(question, context)

        # If no API key → fallback directly
        if not config.OPENAI_API_KEY:
            return self._fallback_response(question, context)

        # Try OpenAI
        return self._call_openai(prompt, question, context)

    def _build_prompt(self, question: str, context: str) -> str:
        """Build structured prompt for HR assistant"""

        return f"""
You are an HR Performance Review Assistant.

Your job:
- Help employees write self-assessments
- Help managers give constructive feedback
- Be clear, professional, and structured

RULES:
- Use bullet points when possible
- Be specific and measurable
- Focus on achievements and improvements

CONTEXT (HR POLICY):
{context}

USER QUESTION:
{question}

ANSWER:
"""

    def _call_openai(self, prompt: str, question: str, context: str) -> str:
        """OpenAI API call using latest SDK"""

        try:
            from openai import OpenAI

            client = OpenAI(api_key=config.OPENAI_API_KEY)

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional HR assistant for performance reviews."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            error_msg = str(e)

            # If quota/rate limit error → fallback
            if "quota" in error_msg.lower() or "rate" in error_msg.lower():
                return self._fallback_response(question, context)

            return f"AI service temporarily unavailable: {error_msg}"

    def _fallback_response(self, question: str, context: str) -> str:
        """Safe fallback when OpenAI is unavailable"""

        if context:
            return (
                "Based on HR policy:\n\n"
                f"{context[:600]}\n\n"
                f"For your question: '{question}', "
                "please refer to the above guidelines and structure your response accordingly."
            )

        return (
            "I couldn't find relevant HR policy information. "
            "Please contact HR for further assistance."
        )