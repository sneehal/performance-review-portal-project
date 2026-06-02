# chatbot_service.py
# Orchestrates the RAG flow: Retrieve → Augment → Generate

from dao.faq_dao import FaqDAO
from services.llm_service import LLMService

faq_dao = FaqDAO()
llm_service = LLMService()


class ChatbotService:

    def answer_question(self, question: str, user_id: int = None) -> dict:
        """
        Full RAG flow:
        1. RETRIEVE: Search relevant FAQs from Oracle DB
        2. AUGMENT: Combine FAQ answers with user's question
        3. GENERATE: Ask LLM to generate a helpful response
        
        Returns:
            dict with 'answer' and 'sources_used' count
        """
        # Step 1: RETRIEVE relevant policy content from DB
        relevant_answers = faq_dao.search_relevant_faqs(question, max_results=3)
        
        # Step 2: AUGMENT — combine retrieved info into context
        if relevant_answers:
            context = "\n\n".join(relevant_answers)
        else:
            # If no specific match, get general policy info
            all_faqs = faq_dao.get_all_faqs()
            context = "\n".join(
                [f"Q: {f['question']}\nA: {f['answer']}" for f in all_faqs[:3]]
            )

        # Step 3: GENERATE response using LLM
        answer = llm_service.generate_response(question=question, context=context)

        return {
            "answer": answer,
            "sources_used": len(relevant_answers),
            "question": question
        }