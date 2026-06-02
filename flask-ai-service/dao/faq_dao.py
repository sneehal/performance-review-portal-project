# faq_dao.py
# Updated to use oracledb

from db import get_connection
from typing import List


class FaqDAO:

    def get_all_faqs(self):
        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT faq_id, question, answer, category
                FROM REVIEW_POLICY_FAQS
                ORDER BY faq_id
            """)

            rows = cursor.fetchall()

            faqs = []

            for r in rows:
                question = r[1].read() if hasattr(r[1], "read") else r[1]
                answer = r[2].read() if hasattr(r[2], "read") else r[2]
                category = r[3].read() if hasattr(r[3], "read") else r[3]

                faqs.append({
                    "faq_id": r[0],
                    "question": str(question),
                    "answer": str(answer),
                    "category": str(category)
                })

            return faqs

        finally:
            if cursor:
                cursor.close()

            if conn:
                conn.close()
            

    def search_relevant_faqs(self, question: str, max_results: int = 3):
        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor()

            words = [
                w.strip().lower()
                for w in question.split()
                if len(w.strip()) > 2
            ]

            if not words:
                return []

            score_parts = []
            params = {}

            for i, w in enumerate(words):
                params[f"kw{i}"] = f"%{w}%"

                score_parts.append(
                    f"CASE WHEN LOWER(question) LIKE :kw{i} THEN 2 ELSE 0 END"
                )
                score_parts.append(
                    f"CASE WHEN LOWER(keywords) LIKE :kw{i} THEN 1 ELSE 0 END"
                )

            score_sql = " + ".join(score_parts)

            sql = f"""
                SELECT answer
                FROM (
                    SELECT answer,
                        ({score_sql}) AS score
                    FROM REVIEW_POLICY_FAQS
                    ORDER BY score DESC, faq_id
                )
                WHERE score > 0
                AND ROWNUM <= :max_results
            """

            params["max_results"] = max_results

            cursor.execute(sql, params)

            rows = cursor.fetchall()

            answers = []
            for r in rows:
                val = r[0]
                if hasattr(val, "read"):
                    val = val.read()
                answers.append(str(val))

            return answers

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
