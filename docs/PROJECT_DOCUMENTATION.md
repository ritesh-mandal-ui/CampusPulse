# CampusPulse — Project Documentation

## 1. Project Overview

CampusPulse is a web-based placement management and analytics system designed to simplify and centralize the campus placement process.

The system provides separate workflows for students and placement administrators. Students can manage their profiles, resumes, skills, job applications, interviews, and offers. TPO/Admin users can manage companies, jobs, applications, interviews, offers, and placement analytics.

CampusPulse also includes a public landing page and analytics dashboards for monitoring placement-related data.

---

## 2. Project Objectives

The main objectives of CampusPulse are:

- Centralize student placement information.
- Manage student profiles, resumes, and skills.
- Allow students to browse and apply for job opportunities.
- Manage companies and job openings.
- Track application progress.
- Schedule and manage interviews.
- Manage placement offers.
- Provide placement analytics to TPO/Admin users.
- Provide a professional public-facing landing page.
- Maintain structured placement data using PostgreSQL.
- Support data analysis through Power BI.

---

## 3. Key Features

### 3.1 Student Features

Students can:

- Register and log in securely.
- View and update their profile.
- View academic information.
- Upload and access their resume.
- Manage technical and professional skills.
- View available job opportunities.
- Check basic job eligibility based on CGPA.
- Apply for jobs.
- Track application status.
- View interview schedules.
- View interview results and remarks.
- View placement offers.

### 3.2 TPO/Admin Features

TPO/Admin users can:

- Access the administrative dashboard.
- Manage companies.
- Create and manage job opportunities.
- View student applications.
- Update application statuses.
- Schedule interviews.
- Record interview results and remarks.
- Create and manage placement offers.
- View placement analytics.

### 3.3 Public Features

Visitors can access:

- CampusPulse landing page.
- Project overview.
- Feature information.
- Placement workflow.
- Public project statistics.
- Login and registration access.

---

## 4. Technology Stack

### Frontend

- HTML5
- CSS3
- JavaScript
- Chart.js
- Responsive UI design

### Backend

- Python
- Flask
- Flask-CORS
- SQLAlchemy
- JWT-based authentication

### Database

- PostgreSQL

### Analytics

- Power BI
- Chart.js

### Development Tools

- Visual Studio Code
- Git
- GitHub
- Python Virtual Environment
- Power BI Desktop

---

## 5. System Architecture

CampusPulse follows a client-server architecture.

```text
                         CampusPulse
                              |
             +----------------+----------------+
             |                                 |
        Frontend                           Backend
     HTML/CSS/JavaScript                    Flask
             |                                 |
             |                            REST API
             |                                 |
             +---------------+-----------------+
                             |
                         PostgreSQL
                             |
              +--------------+--------------+
              |                             |
        Web Analytics                   Power BI
          Chart.js                       Desktop

          Main Components
Frontend

The frontend provides the user interface for:

Public landing page
Login and registration
Student dashboard
Student profile
Student jobs
Student applications
Student interviews
Student offers
Student skills
TPO/Admin dashboard
Company management
Job management
Application management
Interview management
Offer management
Web analytics
Backend

The Flask backend provides:

Authentication
Authorization
Student management
Company management
Job management
Application management
Interview management
Offer management
Analytics
Public statistics
Database

PostgreSQL stores the application's persistent placement data.

6. User Roles

CampusPulse supports the following roles:

Role	Description
STUDENT	Manages profile, skills, resume, jobs, applications, interviews and offers
TPO	Manages placement activities and analytics
ADMIN	Administrative management of placement data
SUPER_ADMIN	Higher-level administrative access

Role-based authorization is implemented on protected backend endpoints.

7. Student Workflow

The main student workflow is:

Register / Login
       |
       v
Student Dashboard
       |
       +----> Profile
       |
       +----> Resume
       |
       +----> Skills
       |
       +----> Jobs
                 |
                 v
              Apply
                 |
                 v
          Application Tracking
                 |
                 v
             Interview
                 |
                 v
               Offer
Profile

Students can view and manage information such as:

Full name
Roll number
Department
CGPA
Graduation year
Phone number
Resume status
Resume

Students can upload a PDF resume and access the uploaded resume from their profile.

Skills

Students can maintain their skills along with proficiency levels such as:

Beginner
Intermediate
Advanced
Jobs

Students can view:

Company
Job title
Minimum CGPA
Maximum backlogs
Salary
Application deadline
Job status

The frontend displays basic eligibility information using the student's CGPA.

Applications

Students can track application statuses such as:

APPLIED
SHORTLISTED
INTERVIEW
SELECTED
REJECTED
WITHDRAWN
Interviews

Students can view:

Interview ID
Application ID
Round
Scheduled time
Mode
Result
Remarks
Offers

Students can view:

Offer ID
Application ID
Salary
Offer date
Offer status
8. TPO/Admin Workflow

The TPO/Admin workflow is:

Login
  |
  v
Admin Dashboard
  |
  +----> Companies
  |
  +----> Jobs
  |
  +----> Applications
  |
  +----> Interviews
  |
  +----> Offers
  |
  +----> Analytics
Company Management

TPO/Admin users can create and manage company information.

Job Management

TPO/Admin users can create job opportunities with information including:

Company
Job title
Job description
Minimum CGPA
Maximum backlogs
Salary
Application deadline
Job status

Supported job statuses:

OPEN
CLOSED
CANCELLED
Application Management

TPO/Admin users can:

View applications.
View student information.
View job and company information.
Update application status.
Interview Management

TPO/Admin users can:

Select an application.
Specify interview round.
Schedule interview date and time.
Select interview mode.
Record result.
Add remarks.

Supported interview modes:

ONLINE
OFFLINE
Offer Management

TPO/Admin users can create offers for selected applications.

Supported offer statuses:

ACTIVE
ACCEPTED
DECLINED
9. Application Lifecycle

A typical placement application follows this workflow:

APPLIED
   |
   v
SHORTLISTED
   |
   v
INTERVIEW
   |
   v
SELECTED
   |
   v
OFFER

Other possible application outcomes include:

APPLIED / SHORTLISTED / INTERVIEW
             |
             v
          REJECTED

or:

APPLIED / SHORTLISTED / INTERVIEW
             |
             v
         WITHDRAWN

The application status is managed by authorized TPO/Admin users.

10. Database Structure

The main PostgreSQL tables used by CampusPulse are:

users
students
departments
skills
student_skills
companies
jobs
applications
interviews
offers
Users

Stores authentication and role information.

Students

Stores student-specific information such as:

Student ID
User relationship
Full name
Roll number
Department
CGPA
Graduation year
Phone
Resume information
Departments

Stores academic department information.

Skills

Stores available skills.

Student Skills

Associates students with their skills and proficiency levels.

Companies

Stores company information.

Jobs

Stores job opportunities posted by companies.

Applications

Stores student applications for jobs.

Interviews

Stores interview schedules and interview information.

Offers

Stores placement offers associated with selected applications.

11. Backend API Modules

The Flask backend is organized into route modules.

Authentication
/api/auth

Handles authentication-related operations.

Students
/api/students

Handles student profile and resume operations.

Companies
/api/companies

Handles company management.

Jobs
/api/jobs

Handles job management.

Applications
/api/applications

Handles job applications and application status updates.

Interviews
/api/interviews

Handles interview scheduling and interview information.

Offers
/api/offers

Handles placement offers.

Analytics
/api/analytics

Provides placement analytics to authorized TPO/Admin users.

Public API
/api/public

Provides public statistics used by the landing page.

Current public summary endpoint:

GET /api/public/summary
12. Authentication and Authorization

CampusPulse uses token-based authentication.

After successful login, the frontend stores the authentication token and uses it when accessing protected API endpoints.

Backend routes use authorization checks to restrict access based on user role.

Examples:

Students can access student-specific resources.
TPO/Admin users can manage placement information.
Analytics endpoints are restricted to authorized administrative roles.
Job creation is restricted to TPO/Admin roles.
Application status updates require administrative authorization.
Interview scheduling requires administrative authorization.
Offer creation requires administrative authorization.
13. Resume Management

CampusPulse supports student resume uploads.

Resume Rules
PDF format is supported.
Maximum file size is 5 MB.
Uploaded resumes are stored under:
backend/uploads/resumes/

The uploaded file is assigned a unique filename.

The application stores the corresponding resume URL with the student's profile.

The upload directory is excluded from Git using:

backend/uploads/

This prevents uploaded student documents from being committed to the repository.

14. Web Analytics

CampusPulse includes a dedicated analytics page for TPO/Admin users.

The web analytics dashboard provides:

Total Students
Total Companies
Total Jobs
Total Applications
Selected Students
Total Offers
Placement Rate
Average Package
Highest Package

It also provides visual analytics for:

Application status
Company-wise placements

The frontend uses Chart.js for data visualization.

The backend provides dedicated analytics endpoints for these metrics.

15. Power BI Analytics

CampusPulse also includes a Power BI analytics dashboard.

Power BI is used as a separate analytics and reporting layer.

The Power BI project file is:

CampusPulse_Analytics.pbix

The dashboard uses placement-related tables including:

applications
companies
departments
interviews
jobs
offers
skills
student_skills
students

The users table is used by the backend authentication system but is not required for the current placement-focused Power BI dashboard.

Power BI Dashboard Areas

The dashboard includes metrics and visualizations such as:

Applications by Status
Jobs by Company
Students by Department
Student Skill Analysis
Applications by Company
Application Trend Over Time
Offers by Company
Interview Results
Jobs by Industry
Average Salary by Company
Applications by Job
Job Status Analysis

Power BI provides a separate analytical view for placement management and reporting.

16. Public Landing Page

CampusPulse includes a professional public landing page.

Files:

frontend/index.html
frontend/css/landing.css
frontend/js/landing.js

The landing page includes:

Navigation bar
Hero section
Call-to-action buttons
Live project statistics
Feature cards
Placement workflow
Analytics section
About section
Final call-to-action
Footer

The landing page retrieves public statistics from:

GET /api/public/summary

The endpoint does not require authentication.

17. Project Structure

The main project structure is:

CampusPulse/
│
├── backend/
│   ├── models/
│   ├── routes/
│   ├── utils/
│   ├── uploads/
│   ├── app.py
│   ├── config.py
│   └── extensions.py
│
├── database/
│   ├── schema.sql
│   ├── seed.sql
│   └── queries.sql
│
├── docs/
│   ├── screenshots/
│   └── PROJECT_DOCUMENTATION.md
│
├── frontend/
│   ├── css/
│   │   ├── landing.css
│   │   └── style.css
│   │
│   ├── js/
│   │   ├── auth.js
│   │   └── landing.js
│   │
│   ├── pages/
│   │   ├── admin-analytics.html
│   │   ├── admin-applications.html
│   │   ├── admin-companies.html
│   │   ├── admin-dashboard.html
│   │   ├── admin-interviews.html
│   │   ├── admin-jobs.html
│   │   ├── admin-offers.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── student-application.html
│   │   ├── student-dashboard.html
│   │   ├── student-interviews.html
│   │   ├── student-jobs.html
│   │   ├── student-offers.html
│   │   ├── student-profile.html
│   │   └── student-skills.html
│   │
│   └── index.html
│
├── powerbi/
│
├── tests/
│
├── CampusPulse_Analytics.pbix
├── README.md
├── requirements.txt
├── .gitignore
└── .env
18. Screenshots

The project documentation includes screenshots demonstrating the major application workflows.

Public and Student Screens
01-landing-page.png
02-login-page.png
03-student-dashboard.png
04-student-profile.png
05-student-jobs.png
06-student-applications.png
07-student-interviews.png
08-student-offers.png
TPO/Admin Screens
09-tpo-dashboard.png
10-job-management.png
11-application-management.png
12-interview-management.png
13-offer-management.png
14-web-analytics.png
Power BI
15-powerbi-dashboard.png

All screenshots are stored in:

docs/screenshots/
19. Security Considerations

CampusPulse includes several security-oriented practices.

Authentication

Protected application areas require authenticated users.

Role-Based Authorization

Backend endpoints verify user roles before performing administrative operations.

Environment Variables

Sensitive configuration is stored outside source code using environment variables.

The .env file is excluded from Git.

Password Security

User passwords are stored using password hashing rather than plain-text storage.

File Upload Protection

Resume uploads are restricted by:

File type
File size
Git Protection

Sensitive and generated files are excluded using .gitignore.

Examples:

.env
venv/
__pycache__/
*.pyc
backend/uploads/
20. Development and Testing

The project was developed and tested locally using a Python virtual environment.

Start Backend
cd C:\CampusPulse
.\venv\Scripts\Activate.ps1
python .\backend\app.py

Backend URL:

http://127.0.0.1:5000
Start Frontend

In another terminal:

cd C:\CampusPulse
python -m http.server 5501 --directory frontend

Frontend URL:

http://127.0.0.1:5501/
Backend Health Check
GET /

Expected response:

{
    "message": "CampusPulse backend is running"
}
Database Test
GET /db-test

This verifies database connectivity.

Model Test
GET /model-test

This verifies that the application's database models are working correctly.

21. End-to-End Testing

The following major workflows were tested:

Student Authentication
Student login
Student dashboard access
Protected student pages
TPO Authentication
TPO login
Administrative dashboard access
Protected administrative pages
Job Application Workflow
Student
   |
   v
View Job
   |
   v
Apply
   |
   v
TPO Reviews Application
   |
   v
Shortlist
   |
   v
Interview
   |
   v
Selected
   |
   v
Offer
Offer Workflow

A complete test flow was performed where a student application progressed through placement stages and an offer was created.

Analytics

Web analytics and Power BI dashboard were verified using the project database.

Landing Page

The public landing page and live summary API were tested successfully.

22. Deployment Plan

CampusPulse is currently structured for local development and can be deployed as a multi-component web application.

A production deployment can include:

User Browser
     |
     v
Frontend Hosting
     |
     v
Flask Backend
     |
     v
Production PostgreSQL
Frontend Deployment

The static frontend can be deployed using a static hosting platform.

Backend Deployment

The Flask backend can be deployed using a Python-compatible hosting platform.

Database Deployment

PostgreSQL can be hosted using a managed database provider.

Production Configuration

Before deployment:

Update database connection variables.
Configure production secret keys.
Update CORS settings.
Update frontend API URL.
Enable HTTPS.
Configure production resume/file storage.
Verify database schema.
Test all authentication and authorization flows.

Power BI can remain a separate analytics/reporting component.

23. Future Enhancements

Possible future improvements include:

Advanced job eligibility based on complete academic records.
Backlog-aware job eligibility enforcement.
Application deadline enforcement.
More controlled application status transitions.
Interview eligibility validation.
Email notifications.
Student notification system.
Advanced search and filtering.
Placement calendar.
Automated placement reports.
More advanced Power BI analytics.
Production deployment.
Cloud-based resume storage.
Mobile-first improvements.
Admin activity logging.
Advanced user and role management.
24. Current Project Status

The major CampusPulse modules are implemented and tested.

Completed
Project structure
PostgreSQL database
Flask backend
Authentication
Role-based authorization
Student management
Resume upload
Skills management
Company management
Job management
Application management
Interview management
Offer management
Web analytics
Power BI analytics
Public landing page
Project README
Project screenshots
Git/GitHub repository
Repository

GitHub repository:

https://github.com/ritesh-mandal-ui/CampusPulse

25. Development Repository

CampusPulse is maintained using Git and GitHub.

The main branch is:

main

The repository contains:

Application source code
Backend API
Frontend pages
Database scripts
Documentation
Screenshots
Power BI project file

Sensitive environment configuration and uploaded resumes are excluded from version control.

26. Conclusion

CampusPulse provides an integrated platform for managing the campus placement lifecycle.

The system connects student management, job opportunities, applications, interviews, offers, and analytics into a single application.

The combination of a Flask REST backend, PostgreSQL database, responsive HTML/CSS/JavaScript frontend, web-based analytics, and Power BI reporting provides a structured foundation for a complete placement management system.

The project is structured for future expansion into a production-ready deployment with cloud hosting, advanced analytics, notifications, and additional placement-management capabilities.

Project Information

Project Name: CampusPulse

Type: Campus Placement Management and Analytics System

Frontend: HTML, CSS, JavaScript

Backend: Python, Flask

Database: PostgreSQL

Analytics: Chart.js and Power BI

Version Control: Git and GitHub

Repository: https://github.com/ritesh-mandal-ui/CampusPulse