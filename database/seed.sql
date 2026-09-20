INSERT INTO departments (department_name, department_code)
VALUES
('Computer Science & Engineering', 'CSE'),
('Computer Science & Engineering (AI)', 'CSE-AI'),
('Electronics & Communication Engineering', 'ECE'),
('Mechanical Engineering', 'ME'),
('Civil Engineering', 'CE');

INSERT INTO users (email, password_hash, role)
VALUES
('ritesh@campuspulse.com', 'demo_hash_1', 'STUDENT'),
('rahul@campuspulse.com', 'demo_hash_2', 'STUDENT'),
('priya@campuspulse.com', 'demo_hash_3', 'STUDENT'),
('aman@campuspulse.com', 'demo_hash_4', 'STUDENT'),
('neha@campuspulse.com', 'demo_hash_5', 'STUDENT'),
('tpo@campuspulse.com', 'demo_hash_6', 'TPO'),
('admin@campuspulse.com', 'demo_hash_7', 'ADMIN');

INSERT INTO students (
    user_id,
    roll_number,
    full_name,
    department_id,
    cgpa,
    graduation_year,
    phone
)
VALUES
(1, 'CSEAI001', 'Ritesh Mandal', 2, 8.12, 2027, '9876500001'),
(2, 'CSEAI002', 'Rahul Kumar', 2, 7.65, 2027, '9876500002'),
(3, 'CSEAI003', 'Priya Singh', 2, 9.01, 2027, '9876500003'),
(4, 'CSE001', 'Aman Kumar', 1, 6.92, 2027, '9876500004'),
(5, 'ECE001', 'Neha Sharma', 3, 8.47, 2027, '9876500005');

INSERT INTO skills (skill_name)
VALUES
('Python'),
('Java'),
('C++'),
('SQL'),
('Machine Learning'),
('Data Analysis'),
('Power BI'),
('JavaScript'),
('HTML/CSS'),
('React'),
('Flask'),
('Git');

INSERT INTO student_skills (student_id, skill_id, proficiency)
VALUES
(1, 1, 'Advanced'),
(1, 4, 'Advanced'),
(1, 5, 'Intermediate'),
(1, 7, 'Intermediate'),
(1, 11, 'Intermediate'),
(1, 12, 'Intermediate'),

(2, 1, 'Intermediate'),
(2, 2, 'Advanced'),
(2, 4, 'Intermediate'),
(2, 8, 'Intermediate'),
(2, 12, 'Intermediate'),

(3, 1, 'Advanced'),
(3, 5, 'Advanced'),
(3, 6, 'Advanced'),
(3, 7, 'Advanced'),
(3, 4, 'Advanced'),

(4, 2, 'Intermediate'),
(4, 3, 'Advanced'),
(4, 4, 'Intermediate'),
(4, 8, 'Intermediate'),

(5, 1, 'Intermediate'),
(5, 4, 'Advanced'),
(5, 6, 'Advanced'),
(5, 7, 'Intermediate');

INSERT INTO companies (
    company_name,
    industry,
    location,
    website
)
VALUES
('Tata Consultancy Services', 'IT Services', 'Bangalore', 'https://www.tcs.com'),
('Infosys', 'IT Services', 'Pune', 'https://www.infosys.com'),
('Accenture', 'IT Consulting', 'Bangalore', 'https://www.accenture.com'),
('Deloitte', 'Consulting', 'Hyderabad', 'https://www.deloitte.com'),
('Wipro', 'IT Services', 'Noida', 'https://www.wipro.com'),
('Amazon', 'E-Commerce & Cloud', 'Bangalore', 'https://www.amazon.com');

INSERT INTO jobs (
    company_id,
    job_title,
    job_description,
    minimum_cgpa,
    maximum_backlogs,
    salary_lpa,
    application_deadline,
    job_status,
    created_by
)
VALUES
(
    1,
    'Graduate Engineer Trainee',
    'Entry-level technology role for engineering graduates.',
    7.00,
    0,
    6.50,
    '2026-10-15 23:59:59',
    'OPEN',
    6
),
(
    2,
    'Systems Engineer',
    'Software development and technology support role.',
    6.50,
    1,
    7.00,
    '2026-10-20 23:59:59',
    'OPEN',
    6
),
(
    3,
    'Associate Software Engineer',
    'Software engineering role involving application development.',
    7.50,
    0,
    8.50,
    '2026-10-25 23:59:59',
    'OPEN',
    6
),
(
    4,
    'Analyst',
    'Business analytics and consulting role.',
    7.00,
    0,
    9.00,
    '2026-11-01 23:59:59',
    'OPEN',
    6
),
(
    5,
    'Project Engineer',
    'Technology and software engineering position.',
    6.50,
    0,
    6.00,
    '2026-11-05 23:59:59',
    'OPEN',
    6
),
(
    6,
    'Software Development Engineer',
    'Software development role for engineering graduates.',
    8.00,
    0,
    18.00,
    '2026-11-10 23:59:59',
    'OPEN',
    6
);

INSERT INTO applications (
    student_id,
    job_id,
    status
)
VALUES
(1, 1, 'SELECTED'),
(1, 3, 'SHORTLISTED'),
(1, 4, 'APPLIED'),

(2, 1, 'SHORTLISTED'),
(2, 2, 'SELECTED'),
(2, 5, 'REJECTED'),

(3, 1, 'SELECTED'),
(3, 3, 'SELECTED'),
(3, 4, 'SHORTLISTED'),
(3, 6, 'SHORTLISTED'),

(4, 1, 'REJECTED'),
(4, 2, 'SHORTLISTED'),
(4, 5, 'APPLIED'),

(5, 2, 'SELECTED'),
(5, 4, 'SELECTED'),
(5, 5, 'SHORTLISTED');

INSERT INTO interviews (
    application_id,
    round_name,
    scheduled_at,
    mode,
    result,
    remarks
)
VALUES
(1, 'Technical Interview', '2026-09-05 10:00:00', 'ONLINE', 'PASSED', 'Good technical fundamentals'),
(1, 'HR Interview', '2026-09-07 11:00:00', 'ONLINE', 'PASSED', 'Selected'),

(2, 'Technical Interview', '2026-09-10 14:00:00', 'ONLINE', 'PENDING', NULL),

(4, 'Technical Interview', '2026-09-08 10:30:00', 'OFFLINE', 'PASSED', 'Shortlisted for HR'),

(5, 'Technical Interview', '2026-09-06 12:00:00', 'ONLINE', 'PASSED', 'Selected'),

(7, 'Technical Interview', '2026-09-04 15:00:00', 'ONLINE', 'PASSED', 'Selected'),

(8, 'Technical Interview', '2026-09-09 11:00:00', 'ONLINE', 'PASSED', 'Selected'),

(9, 'Technical Interview', '2026-09-12 13:00:00', 'OFFLINE', 'PENDING', NULL),

(10, 'Technical Interview', '2026-09-13 10:00:00', 'ONLINE', 'PENDING', NULL),

(14, 'Technical Interview', '2026-09-14 14:00:00', 'OFFLINE', 'PASSED', 'Selected');

INSERT INTO offers (
    application_id,
    salary_lpa,
    offer_date,
    offer_status
)
VALUES
(1, 6.50, '2026-09-08', 'ACCEPTED'),
(5, 7.00, '2026-09-07', 'ACCEPTED'),
(7, 6.50, '2026-09-06', 'ACCEPTED'),
(8, 8.50, '2026-09-10', 'ACTIVE'),
(14, 9.00, '2026-09-15', 'ACCEPTED');