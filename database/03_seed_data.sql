-- ============================================================
-- Seed Data: Competencies, FAQs, and Sample Review Cycle
-- ============================================================

-- Competencies
INSERT INTO COMPETENCIES (name, description, is_active) 
VALUES ('Communication', 'Ability to convey ideas clearly and listen effectively', 1);

INSERT INTO COMPETENCIES (name, description, is_active) 
VALUES ('Technical Skills', 'Proficiency in required tools and technologies', 1);

INSERT INTO COMPETENCIES (name, description, is_active) 
VALUES ('Teamwork', 'Collaboration, cooperation, and team contribution', 1);

INSERT INTO COMPETENCIES (name, description, is_active) 
VALUES ('Problem Solving', 'Analytical thinking and decision-making ability', 1);

INSERT INTO COMPETENCIES (name, description, is_active) 
VALUES ('Leadership', 'Ability to guide, motivate, and inspire others', 1);

INSERT INTO COMPETENCIES (name, description, is_active) 
VALUES ('Time Management', 'Meeting deadlines and prioritizing effectively', 1);

-- Review Policy FAQs (used by AI chatbot RAG)
INSERT INTO REVIEW_POLICY_FAQS (question, answer, category, keywords)
VALUES (
    'What does a rating of 5 mean?',
    'A rating of 5 means Exceptional. The employee consistently exceeded all targets and demonstrated outstanding performance beyond expectations.',
    'Rating Scale',
    'rating,5,exceptional,outstanding,exceeded'
);

INSERT INTO REVIEW_POLICY_FAQS (question, answer, category, keywords)
VALUES (
    'What does a rating of 4 mean?',
    'A rating of 4 means Exceeds Expectations. The employee met all targets and frequently exceeded them in key areas.',
    'Rating Scale',
    'rating,4,exceeds,expectations'
);

INSERT INTO REVIEW_POLICY_FAQS (question, answer, category, keywords)
VALUES (
    'What does a rating of 3 mean?',
    'A rating of 3 means Meets Expectations. The employee consistently met all performance targets and fulfilled their role responsibilities.',
    'Rating Scale',
    'rating,3,meets,expectations,average'
);

INSERT INTO REVIEW_POLICY_FAQS (question, answer, category, keywords)
VALUES (
    'What does a rating of 2 mean?',
    'A rating of 2 means Needs Improvement. The employee partially met targets but requires coaching and support in key areas.',
    'Rating Scale',
    'rating,2,needs,improvement,below'
);

INSERT INTO REVIEW_POLICY_FAQS (question, answer, category, keywords)
VALUES (
    'What does a rating of 1 mean?',
    'A rating of 1 means Unsatisfactory. The employee did not meet the required performance targets and may be placed on a Performance Improvement Plan (PIP).',
    'Rating Scale',
    'rating,1,unsatisfactory,pip,poor'
);

INSERT INTO REVIEW_POLICY_FAQS (question, answer, category, keywords)
VALUES (
    'What is the self-assessment deadline?',
    'The self-assessment must be submitted at least 2 weeks before the cycle end date. Late submissions are flagged to HR automatically.',
    'Deadlines',
    'deadline,self-assessment,submit,due date'
);

INSERT INTO REVIEW_POLICY_FAQS (question, answer, category, keywords)
VALUES (
    'How are goals weighted?',
    'Each goal has a weight percentage. All goal weights must sum to exactly 100%. Higher-weight goals have more impact on the final score. For example, a goal with 40% weight has twice the impact of a 20% weight goal.',
    'Goals',
    'goals,weight,percentage,100,impact,score'
);

INSERT INTO REVIEW_POLICY_FAQS (question, answer, category, keywords)
VALUES (
    'What is a PIP recommendation?',
    'PIP stands for Performance Improvement Plan. It is assigned to employees rated below 2.0. HR will schedule a meeting to discuss a structured improvement plan with timelines and targets.',
    'Recommendations',
    'pip,performance,improvement,plan,below,2'
);

INSERT INTO REVIEW_POLICY_FAQS (question, answer, category, keywords)
VALUES (
    'How is the final score calculated?',
    'Each goal score is multiplied by its weight percentage and divided by 100. All these weighted scores are summed to get the final score out of 5. Example: Goal A (score 4, weight 40%) = 1.60, Goal B (score 3, weight 60%) = 1.80. Total = 3.40 out of 5.',
    'Goals',
    'final,score,calculation,weighted,formula'
);

INSERT INTO REVIEW_POLICY_FAQS (question, answer, category, keywords)
VALUES (
    'How to write a good self-assessment?',
    'A good self-assessment should: 1) Reference specific achievements with measurable results, 2) Use action verbs like delivered, improved, reduced, increased, 3) Be honest about challenges faced, 4) Align with your goals set at the start of the cycle, 5) Avoid vague statements like worked hard or did my best.',
    'Feedback',
    'self-assessment,write,good,tips,how to,feedback'
);

COMMIT;