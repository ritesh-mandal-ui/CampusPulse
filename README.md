# CampusPulse

CampusPulse is a web-based placement management system designed to simplify and centralize the placement activities of students, companies, and placement administrators.

The system provides a centralized platform for managing student profiles, skills, job opportunities, applications, interviews, placement offers, and placement analytics.

## Project Overview

Traditional placement management often involves maintaining student information, job applications, interview schedules, and placement records across multiple systems or spreadsheets.

CampusPulse brings these activities together into a single web-based system.

The application provides separate functionality for students and placement administrators, along with role-based authentication and access control.

## Key Features

### Student Management

* Student registration and authentication
* Student profile creation and management
* Department information
* Skill management
* Resume upload and management
* View available job opportunities
* Apply for eligible jobs
* Track submitted applications
* View interview information
* View placement offers

### Company Management

* Add and manage companies
* Store company information
* Associate companies with job opportunities
* View company-related placement information

### Job Management

* Create and manage job opportunities
* Associate jobs with companies
* Define job-related eligibility information
* View available jobs
* Track job applications

### Application Management

* Students can apply for jobs
* Track application status
* Placement administrators can manage applications
* Application statuses include:

APPLIED
SHORTLISTED
INTERVIEW
SELECTED
REJECTED
WITHDRAWN

### Interview Management

* Manage student interviews
* Store interview details
* Support online and offline interview modes
* Track interview results

Interview results include:

PENDING
PASSED
FAILED

### Offer Management

* Create placement offers for selected applications
* Store salary/package information
* Store offer dates
* Track offer status

Offer statuses include:

ACTIVE
ACCEPTED
DECLINED

### Placement Analytics

CampusPulse provides placement-related analytics through both the web application and Microsoft Power BI.

The analytics system provides information such as:

* Total students
* Total companies
* Total jobs
* Total applications
* Selected students
* Total offers
* Placement rate
* Average package
* Highest package
* Application status distribution
* Company-wise selected student information

## Technology Stack

### Backend

* Python
* Flask
* Flask-SQLAlchemy
* Flask-CORS
* PyJWT
* bcrypt
* python-dotenv

### Database

* PostgreSQL
* SQLAlchemy ORM

### Frontend

* HTML5
* CSS3
* JavaScript

### Analytics

* Microsoft Power BI
* CampusPulse Web Analytics
* Chart.js

## Authentication and Authorization

CampusPulse uses JWT-based authentication for protected API endpoints.

During registration, user passwords are hashed using bcrypt before being stored in the database.

After successful login, the backend generates a JWT token containing the authenticated user's information and role.

Protected API requests use the following authorization format:

Authorization: Bearer <token>

The system uses role-based access control for different types of users.

## User Roles

### STUDENT

Students can:

* Manage their profile
* Upload and manage their resume
* Manage their skills
* Browse available jobs
* Apply for jobs
* Track applications
* View interviews
* View placement offers

### TPO

TPO users can access placement-management functionality and placement analytics.

### ADMIN

Admin users can manage:

* Companies
* Jobs
* Applications
* Interviews
* Offers
* Placement analytics

### SUPER_ADMIN

Super Admin functionality is supported by the backend for administrative access.

## API Structure

The backend is organized into separate route modules.

### Authentication

`/api/auth`

Available operations:

* POST `/api/auth/register`
* POST `/api/auth/login`
* GET `/api/auth/me`

### Students

`/api/students`

Handles student profiles, resume management, and student-related information.

### Jobs

`/api/jobs`

Handles job opportunities and job-related operations.

### Applications

`/api/applications`

Handles job applications and application status management.

### Companies

`/api/companies`

Handles company information.

### Interviews

`/api/interviews`

Handles interview information and interview results.

### Offers

`/api/offers`

Handles placement offers.

### Analytics

`/api/analytics`

Provides placement summaries, application-status information, and company placement information.

## Project Structure

```text
CampusPulse/
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── extensions.py
│   │
│   ├── models/
│   │   ├── application.py
│   │   ├── company.py
│   │   ├── department.py
│   │   ├── interview.py
│   │   ├── job.py
│   │   ├── offer.py
│   │   ├── skill.py
│   │   ├── student.py
│   │   ├── student_skill.py
│   │   └── user.py
│   │
│   ├── routes/
│   │   ├── analytics.py
│   │   ├── applications.py
│   │   ├── auth.py
│   │   ├── companies.py
│   │   ├── interviews.py
│   │   ├── jobs.py
│   │   ├── offers.py
│   │   └── students.py
│   │
│   └── utils/
│       └── decorators.py
│
├── database/
│   ├── schema.sql
│   ├── seed.sql
│   └── queries.sql
│
├── docs/
│   └── screenshots/
│
├── frontend/
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   └── auth.js
│   │
│   └── pages/
│       ├── login.html
│       ├── register.html
│       ├── student-dashboard.html
│       ├── student-profile.html
│       ├── student-skills.html
│       ├── student-jobs.html
│       ├── student-application.html
│       ├── student-interviews.html
│       ├── student-offers.html
│       ├── admin-dashboard.html
│       ├── admin-companies.html
│       ├── admin-jobs.html
│       ├── admin-applications.html
│       ├── admin-interviews.html
│       ├── admin-offers.html
│       └── admin-analytics.html
│
├── powerbi/
│
├── tests/
│
├── CampusPulse_Analytics.pbix
├── requirements.txt
├── .gitignore
└── README.md