# CampusPulse

CampusPulse is a web-based placement management system designed to simplify and centralize the placement activities of students, companies, and placement administrators.

The system provides a centralized platform for managing student profiles, skills, job opportunities, applications, interviews, placement offers, and placement analytics.

## Project Overview

Traditional placement management often involves maintaining student information, job applications, interview schedules, and placement records across multiple systems or spreadsheets.

CampusPulse aims to bring these activities together into a single web-based system.

The application provides separate functionality for students and placement administrators, along with role-based authentication and access control.

## Key Features

### Student Management

* Student registration and authentication
* Student profile creation and management
* Department information
* Skill management
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

/api/auth

Available operations:

POST /api/auth/register
POST /api/auth/login
GET /api/auth/me

### Students

/api/students

Handles student profiles and student-related information.

### Jobs

/api/jobs

Handles job opportunities and job-related operations.

### Applications

/api/applications

Handles job applications and application status management.

### Companies

/api/companies

Handles company information.

### Interviews

/api/interviews

Handles interview information and interview results.

### Offers

/api/offers

Handles placement offers.

### Analytics

/api/analytics

Provides placement summaries, application-status information, and company placement information.

## Project Structure

CampusPulse/
│
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
├── CampusPulse_Analytics.pbix
├── requirements.txt
├── .env
├── .gitignore
└── README.md

## Database Design

CampusPulse uses PostgreSQL as its primary database.

The database is organized around the following major entities:

### Users

Stores authentication information and user roles.

### Students

Stores student profile information and academic details.

### Departments

Stores department information associated with students.

### Skills

Stores available student skills.

### Student Skills

Associates students with their skills and proficiency levels.

### Companies

Stores company information.

### Jobs

Stores job opportunities and eligibility requirements.

### Applications

Stores student applications for available jobs.

### Interviews

Stores interview information related to applications.

### Offers

Stores placement offers associated with selected applications.

The database schema is available in:

database/schema.sql

Initial/demo database records are available in:

database/seed.sql

The seed file represents the initial sample dataset and is not intended to be a live snapshot of the current development database.

Useful SQL queries are available in:

database/queries.sql

## Setup and Installation

### 1. Clone the Repository

git clone <repository-url>
cd CampusPulse

Replace <repository-url> with the actual repository URL when the project repository is finalized.

### 2. Create a Virtual Environment

On Windows:

python -m venv venv

Activate the virtual environment:

venv\Scripts\activate

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Configure Environment Variables

Create a .env file in the project root.

Example:

DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key

DATABASE_URL should contain the PostgreSQL database connection string.

SECRET_KEY should contain a strong secret value used for application authentication.

Do not commit the .env file to Git.

### 5. Configure the Database

Create a PostgreSQL database and execute:

database/schema.sql

If the initial sample data is required, execute:

database/seed.sql

### 6. Start the Backend

From the project root:

python backend/app.py

For local development, the Flask backend is available at:

http://127.0.0.1:5000

### 7. Start the Frontend

Open a separate terminal from the project root and run:

python -m http.server 5500 --directory frontend

The frontend is then available at:

http://127.0.0.1:5500

The login page is:

http://127.0.0.1:5500/pages/login.html

## Environment Variables

The application uses environment variables for configuration.

DATABASE_URL
PostgreSQL database connection URL.

SECRET_KEY
Secret key used for authentication.

Sensitive configuration values should never be committed to the repository.

## Power BI Analytics

CampusPulse includes a dedicated Microsoft Power BI dashboard for advanced placement analytics.

The Power BI project file is:

CampusPulse_Analytics.pbix

The project contains two analytics layers.

### CampusPulse Web Analytics

The web application provides placement analytics through:

frontend/pages/admin-analytics.html

This dashboard provides information such as:

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
* Company-wise placements

### Microsoft Power BI Dashboard

The Power BI dashboard provides a separate business-intelligence and reporting layer for placement data.

It can be used for:

* Placement overview
* Application analysis
* Application status distribution
* Company-wise placement analysis
* Placement-related visual reporting
* Interactive data exploration

The Power BI dashboard is maintained separately from the CampusPulse web interface through the .pbix project file.

## Security

CampusPulse includes several basic security mechanisms:

* Password hashing using bcrypt
* JWT-based authentication
* Bearer-token authentication for protected APIs
* Role-based authorization
* Environment variables for sensitive configuration
* .env excluded from version control
* Validation of authenticated users on protected endpoints

## Development Workflow

A typical development workflow is:

1. Start the PostgreSQL database.
2. Activate the Python virtual environment.
3. Configure the .env file.
4. Install project dependencies.
5. Start the Flask backend.
6. Start the frontend HTTP server.
7. Open the login page.
8. Test authentication.
9. Test student functionality.
10. Test administrative functionality.
11. Verify application, interview, and offer workflows.
12. Verify placement analytics.
13. Verify the Power BI dashboard.

## Future Enhancements

Possible future improvements include:

* Email notifications for application and interview updates
* Automated eligibility checking
* Resume upload and management
* Advanced student-job matching
* Automated placement reports
* Additional Power BI dashboards
* More detailed administrative permissions
* Application history and activity tracking
* Improved deployment and production configuration

## License

This project is developed for educational and academic purposes.