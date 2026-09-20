CREATE TABLE departments (
    department_id BIGSERIAL PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL,
    department_code VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE users (
    user_id BIGSERIAL PRIMARY KEY,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('STUDENT', 'TPO', 'ADMIN', 'SUPER_ADMIN')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE students (
    student_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL UNIQUE,
    roll_number VARCHAR(50) NOT NULL UNIQUE,
    full_name VARCHAR(150) NOT NULL,
    department_id BIGINT NOT NULL,
    cgpa NUMERIC(3,2) CHECK (cgpa >= 0 AND cgpa <= 10),
    graduation_year INT,
    phone VARCHAR(20),
    resume_url TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_students_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_students_department
        FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
);

CREATE TABLE skills (
    skill_id BIGSERIAL PRIMARY KEY,
    skill_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE student_skills (
    student_id BIGINT NOT NULL,
    skill_id BIGINT NOT NULL,
    proficiency VARCHAR(30),

    PRIMARY KEY (student_id, skill_id),

    CONSTRAINT fk_student_skills_student
        FOREIGN KEY (student_id)
        REFERENCES students(student_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_student_skills_skill
        FOREIGN KEY (skill_id)
        REFERENCES skills(skill_id)
        ON DELETE CASCADE
);

CREATE TABLE companies (
    company_id BIGSERIAL PRIMARY KEY,
    company_name VARCHAR(150) NOT NULL,
    industry VARCHAR(100),
    location VARCHAR(150),
    website TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE jobs (
    job_id BIGSERIAL PRIMARY KEY,
    company_id BIGINT NOT NULL,
    job_title VARCHAR(150) NOT NULL,
    job_description TEXT,
    minimum_cgpa NUMERIC(3,2) CHECK (minimum_cgpa >= 0 AND minimum_cgpa <= 10),
    maximum_backlogs INT NOT NULL DEFAULT 0 CHECK (maximum_backlogs >= 0),
    salary_lpa NUMERIC(10,2) CHECK (salary_lpa >= 0),
    application_deadline TIMESTAMP,
    job_status VARCHAR(30) NOT NULL DEFAULT 'OPEN'
        CHECK (job_status IN ('OPEN', 'CLOSED', 'CANCELLED')),
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_jobs_company
        FOREIGN KEY (company_id)
        REFERENCES companies(company_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_jobs_created_by
        FOREIGN KEY (created_by)
        REFERENCES users(user_id)
);

CREATE TABLE applications (
    application_id BIGSERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL,
    job_id BIGINT NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'APPLIED'
        CHECK (status IN (
            'APPLIED',
            'SHORTLISTED',
            'INTERVIEW',
            'REJECTED',
            'SELECTED',
            'WITHDRAWN'
        )),
    applied_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT unique_student_job
        UNIQUE (student_id, job_id),

    CONSTRAINT fk_applications_student
        FOREIGN KEY (student_id)
        REFERENCES students(student_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_applications_job
        FOREIGN KEY (job_id)
        REFERENCES jobs(job_id)
        ON DELETE CASCADE
);

CREATE TABLE interviews (
    interview_id BIGSERIAL PRIMARY KEY,
    application_id BIGINT NOT NULL,
    round_name VARCHAR(100) NOT NULL,
    scheduled_at TIMESTAMP NOT NULL,
    mode VARCHAR(30) NOT NULL
        CHECK (mode IN ('ONLINE', 'OFFLINE')),
    result VARCHAR(30)
        CHECK (result IN ('PENDING', 'PASSED', 'FAILED')),
    remarks TEXT,

    CONSTRAINT fk_interviews_application
        FOREIGN KEY (application_id)
        REFERENCES applications(application_id)
        ON DELETE CASCADE
);

CREATE TABLE offers (
    offer_id BIGSERIAL PRIMARY KEY,
    application_id BIGINT NOT NULL UNIQUE,
    salary_lpa NUMERIC(10,2) NOT NULL CHECK (salary_lpa >= 0),
    offer_date DATE NOT NULL DEFAULT CURRENT_DATE,
    offer_status VARCHAR(30) NOT NULL DEFAULT 'ACTIVE'
        CHECK (offer_status IN ('ACTIVE', 'ACCEPTED', 'DECLINED')),

    CONSTRAINT fk_offers_application
        FOREIGN KEY (application_id)
        REFERENCES applications(application_id)
        ON DELETE CASCADE
);

CREATE INDEX idx_students_department
    ON students(department_id);

CREATE INDEX idx_student_skills_skill
    ON student_skills(skill_id);

CREATE INDEX idx_jobs_company
    ON jobs(company_id);

CREATE INDEX idx_jobs_status
    ON jobs(job_status);

CREATE INDEX idx_applications_student
    ON applications(student_id);

CREATE INDEX idx_applications_job
    ON applications(job_id);

CREATE INDEX idx_applications_status
    ON applications(status);

CREATE INDEX idx_interviews_application
    ON interviews(application_id);

CREATE INDEX idx_interviews_scheduled_at
    ON interviews(scheduled_at);

CREATE INDEX idx_offers_application
    ON offers(application_id);