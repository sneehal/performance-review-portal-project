-- ============================================================
-- Sample Test Users (for development and testing)
-- Passwords are bcrypt hashed
-- Plain text passwords:
--   HR Admin   → Admin@123
--   Manager    → Manager@123
--   Employee 1 → Employee@123
--   Employee 2 → Employee@123
-- ============================================================

-- HR Admin user (no manager_id needed)
INSERT INTO USERS (name, email, password_hash, role, department, manager_id)
VALUES (
    'Sarah HR Admin',
    'sarah.hr@company.com',
    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',
    'hr_admin',
    'Human Resources',
    NULL
);

-- Manager (reports to no one for now)
INSERT INTO USERS (name, email, password_hash, role, department, manager_id)
VALUES (
    'Mike Manager',
    'mike.manager@company.com',
    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',
    'manager',
    'Engineering',
    NULL
);

-- Employee 1 (reports to Mike Manager → user_id 2)
INSERT INTO USERS (name, email, password_hash, role, department, manager_id)
VALUES (
    'Alice Employee',
    'alice.emp@company.com',
    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',
    'employee',
    'Engineering',
    2
);

-- Employee 2 (reports to Mike Manager → user_id 2)
INSERT INTO USERS (name, email, password_hash, role, department, manager_id)
VALUES (
    'Bob Employee',
    'bob.emp@company.com',
    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',
    'employee',
    'Engineering',
    2
);

-- Sample Review Cycle (created by Sarah HR Admin → user_id 1)
INSERT INTO REVIEW_CYCLES (name, start_date, end_date, self_due_date, manager_due_date, status, created_by)
VALUES (
    'Q1 2025 Appraisal',
    DATE '2025-01-01',
    DATE '2025-03-31',
    DATE '2025-03-15',
    DATE '2025-03-28',
    'Active',
    1
);

COMMIT;