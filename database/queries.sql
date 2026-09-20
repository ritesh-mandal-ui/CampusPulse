SELECT
    s.student_id,
    s.roll_number,
    s.full_name,
    u.email,
    d.department_name,
    s.cgpa,
    s.graduation_year,
    s.phone
FROM students s
JOIN users u
    ON s.user_id = u.user_id
LEFT JOIN departments d
    ON s.department_id = d.department_id
ORDER BY s.student_id;


-- 2. View all companies
SELECT
    company_id,
    company_name,
    industry,
    location,
    website
FROM companies
ORDER BY company_id;


-- 3. View available jobs with company information
SELECT
    j.job_id,
    j.job_title,
    c.company_name,
    j.minimum_cgpa,
    j.maximum_backlogs,
    j.salary_lpa,
    j.application_deadline,
    j.job_status
FROM jobs j
JOIN companies c
    ON j.company_id = c.company_id
ORDER BY j.job_id;


-- 4. Application status summary
SELECT
    status,
    COUNT(*) AS application_count
FROM applications
GROUP BY status
ORDER BY status;


-- 5. Student-wise application details
SELECT
    s.student_id,
    s.full_name AS student_name,
    j.job_title,
    c.company_name,
    a.status,
    a.applied_at
FROM applications a
JOIN students s
    ON a.student_id = s.student_id
JOIN jobs j
    ON a.job_id = j.job_id
JOIN companies c
    ON j.company_id = c.company_id
ORDER BY s.student_id, a.applied_at DESC;


-- 6. Company-wise application count
SELECT
    c.company_id,
    c.company_name,
    COUNT(a.application_id) AS application_count
FROM companies c
LEFT JOIN jobs j
    ON c.company_id = j.company_id
LEFT JOIN applications a
    ON j.job_id = a.job_id
GROUP BY c.company_id, c.company_name
ORDER BY application_count DESC, c.company_name;


-- 7. Selected students and their placement details
SELECT
    s.student_id,
    s.full_name AS student_name,
    c.company_name,
    j.job_title,
    o.salary_lpa,
    o.offer_date,
    o.offer_status
FROM offers o
JOIN applications a
    ON o.application_id = a.application_id
JOIN students s
    ON a.student_id = s.student_id
JOIN jobs j
    ON a.job_id = j.job_id
JOIN companies c
    ON j.company_id = c.company_id
WHERE a.status = 'SELECTED'
ORDER BY o.salary_lpa DESC;


-- 8. Placement package summary
SELECT
    COUNT(*) AS total_offers,
    ROUND(AVG(salary_lpa), 2) AS average_package_lpa,
    MAX(salary_lpa) AS highest_package_lpa,
    MIN(salary_lpa) AS lowest_package_lpa
FROM offers;