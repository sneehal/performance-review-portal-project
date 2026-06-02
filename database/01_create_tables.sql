-- ============================================================
-- AI-Powered Performance Review Portal
-- Oracle Database Schema
-- Run this file first before anything else
-- ============================================================

-- Drop tables if they exist (for fresh setup)
-- Run in reverse order to avoid FK constraint errors
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE COMPETENCY_RATINGS CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE COMPETENCIES CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE FEEDBACK CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE RATINGS CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE REVIEWS CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE GOALS CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE REVIEW_CYCLES CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE REVIEW_POLICY_FAQS CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE USERS CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL; END;
/

-- ============================================================
-- TABLE 1: USERS
-- Stores all users: employees, managers, hr_admin
-- manager_id is self-referencing FK (employee -> their manager)
-- ============================================================
CREATE TABLE USERS (
    user_id        NUMBER          PRIMARY KEY,
    name           VARCHAR2(100)   NOT NULL,
    email          VARCHAR2(150)   UNIQUE NOT NULL,
    password_hash  VARCHAR2(255)   NOT NULL,
    role           VARCHAR2(20)    DEFAULT 'employee' NOT NULL,
                                   -- Values: employee, manager, hr_admin
    department     VARCHAR2(100),
    manager_id     NUMBER,         -- Self-referencing FK
    is_active      NUMBER(1)       DEFAULT 1,
    created_at     TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_users_manager FOREIGN KEY (manager_id) REFERENCES USERS(user_id),
    CONSTRAINT chk_user_role CHECK (role IN ('employee', 'manager', 'hr_admin'))
);

-- ============================================================
-- TABLE 2: REVIEW_CYCLES
-- HR creates review cycles like "Q1 2025 Appraisal"
-- ============================================================
CREATE TABLE REVIEW_CYCLES (
    cycle_id          NUMBER        PRIMARY KEY,
    name              VARCHAR2(100) NOT NULL,
    start_date        DATE          NOT NULL,
    end_date          DATE          NOT NULL,
    self_due_date     DATE          NOT NULL,   -- Employee must submit by this date
    manager_due_date  DATE          NOT NULL,   -- Manager must review by this date
    status            VARCHAR2(20)  DEFAULT 'Draft' NOT NULL,
                                                -- Draft, Active, Closed
    created_by        NUMBER        NOT NULL,
    created_at        TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_cycle_creator FOREIGN KEY (created_by) REFERENCES USERS(user_id),
    CONSTRAINT chk_cycle_status CHECK (status IN ('Draft', 'Active', 'Closed'))
);

-- ============================================================
-- TABLE 3: GOALS
-- Each employee sets goals per review cycle
-- weight must total 100% per user per cycle
-- ============================================================
CREATE TABLE GOALS (
    goal_id      NUMBER          PRIMARY KEY,
    user_id      NUMBER          NOT NULL,
    cycle_id     NUMBER          NOT NULL,
    title        VARCHAR2(200)   NOT NULL,
    description  CLOB,           -- Long text allowed
    weight       NUMBER(5,2)     NOT NULL,  -- e.g., 40.00 means 40%
    target       VARCHAR2(300),
    achievement  VARCHAR2(300),  -- Filled in at review time
    created_at   TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_goal_user  FOREIGN KEY (user_id)  REFERENCES USERS(user_id),
    CONSTRAINT fk_goal_cycle FOREIGN KEY (cycle_id) REFERENCES REVIEW_CYCLES(cycle_id),
    CONSTRAINT chk_weight    CHECK (weight > 0 AND weight <= 100)
);

-- ============================================================
-- TABLE 4: REVIEWS
-- One review record per employee per cycle per type
-- type: SELF (employee submits) or MANAGER (manager submits)
-- ============================================================
CREATE TABLE REVIEWS (
    review_id       NUMBER        PRIMARY KEY,
    user_id         NUMBER        NOT NULL,   -- Employee being reviewed
    cycle_id        NUMBER        NOT NULL,
    type            VARCHAR2(20)  NOT NULL,   -- SELF or MANAGER
    status          VARCHAR2(20)  DEFAULT 'Draft' NOT NULL,
                                              -- Draft, Submitted, Completed
    overall_comment CLOB,
    submitted_at    TIMESTAMP,
    created_at      TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_review_user  FOREIGN KEY (user_id)  REFERENCES USERS(user_id),
    CONSTRAINT fk_review_cycle FOREIGN KEY (cycle_id) REFERENCES REVIEW_CYCLES(cycle_id),
    CONSTRAINT chk_review_type   CHECK (type IN ('SELF', 'MANAGER')),
    CONSTRAINT chk_review_status CHECK (status IN ('Draft', 'Submitted', 'Completed')),
    -- Prevent duplicate submissions: one SELF review per user per cycle
    CONSTRAINT uq_review UNIQUE (user_id, cycle_id, type)
);

-- ============================================================
-- TABLE 5: RATINGS
-- Individual goal scores inside a review
-- ============================================================
CREATE TABLE RATINGS (
    rating_id  NUMBER          PRIMARY KEY,
    review_id  NUMBER          NOT NULL,
    goal_id    NUMBER          NOT NULL,
    score      NUMBER(2,1)     NOT NULL,  -- 1.0 to 5.0
    comment    VARCHAR2(500),
    rated_by   NUMBER          NOT NULL,  -- user_id of who rated
    CONSTRAINT fk_rating_review FOREIGN KEY (review_id) REFERENCES REVIEWS(review_id),
    CONSTRAINT fk_rating_goal   FOREIGN KEY (goal_id)   REFERENCES GOALS(goal_id),
    CONSTRAINT fk_rating_user   FOREIGN KEY (rated_by)  REFERENCES USERS(user_id),
    CONSTRAINT chk_score CHECK (score >= 1 AND score <= 5)
);

-- ============================================================
-- TABLE 6: FEEDBACK
-- Manager's overall written feedback on an employee
-- ============================================================
CREATE TABLE FEEDBACK (
    feedback_id     NUMBER          PRIMARY KEY,
    review_id       NUMBER          NOT NULL,
    reviewer_id     NUMBER          NOT NULL,  -- Manager's user_id
    feedback_text   CLOB            NOT NULL,
    overall_rating  NUMBER(2,1)     NOT NULL,
    recommendation  VARCHAR2(50),  -- Promote, Excellent, PIP, etc.
    created_at      TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_feedback_review   FOREIGN KEY (review_id)   REFERENCES REVIEWS(review_id),
    CONSTRAINT fk_feedback_reviewer FOREIGN KEY (reviewer_id) REFERENCES USERS(user_id),
    CONSTRAINT chk_overall_rating   CHECK (overall_rating >= 1 AND overall_rating <= 5)
);

-- ============================================================
-- TABLE 7: COMPETENCIES
-- HR-defined company competencies
-- ============================================================
CREATE TABLE COMPETENCIES (
    comp_id      NUMBER          PRIMARY KEY,
    name         VARCHAR2(100)   NOT NULL,
    description  VARCHAR2(300),
    is_active    NUMBER(1)       DEFAULT 1,  -- 1=active, 0=disabled
    CONSTRAINT chk_comp_active CHECK (is_active IN (0, 1))
);

-- ============================================================
-- TABLE 8: COMPETENCY_RATINGS
-- Employee and manager both rate competencies separately
-- ============================================================
CREATE TABLE COMPETENCY_RATINGS (
    cr_id      NUMBER          PRIMARY KEY,
    review_id  NUMBER          NOT NULL,
    comp_id    NUMBER          NOT NULL,
    score      NUMBER(2,1)     NOT NULL,
    rated_by   NUMBER          NOT NULL,
    comment    VARCHAR2(300),
    CONSTRAINT fk_cr_review FOREIGN KEY (review_id) REFERENCES REVIEWS(review_id),
    CONSTRAINT fk_cr_comp   FOREIGN KEY (comp_id)   REFERENCES COMPETENCIES(comp_id),
    CONSTRAINT fk_cr_user   FOREIGN KEY (rated_by)  REFERENCES USERS(user_id),
    CONSTRAINT chk_cr_score CHECK (score >= 1 AND score <= 5)
);

-- ============================================================
-- TABLE 9: REVIEW_POLICY_FAQS
-- Used by the Flask AI chatbot for RAG (search + LLM)
-- ============================================================
CREATE TABLE REVIEW_POLICY_FAQS (
    faq_id    NUMBER          PRIMARY KEY,
    question  VARCHAR2(500)   NOT NULL,
    answer    CLOB            NOT NULL,
    category  VARCHAR2(100),  -- Rating Scale, Deadlines, Goals, Feedback
    keywords  VARCHAR2(300)   -- Comma-separated keywords for search
);

COMMIT;