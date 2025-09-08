# Job Management API

## Overview

This Django REST Framework project provides a **Job and Task Management API** for a company with the following roles:

- **Admin**
- **Technician**
- **SalesAgent**

The system also includes **Equipment management** and an **AuditLog** to track changes.

---

## Features

- Custom User model using email as login.
- Role-based access control.
- Jobs with nested tasks.
- Equipment assignment to tasks.
- Technician dashboard showing assigned tasks grouped by scheduled date.
- Audit log for all job/task actions.
- Filtering and ordering of jobs and tasks.
- JWT authentication with **1-day access token lifetime**.

---

## Installation

### Using Docker

1. Clone repository:
- git clone https://github.com/najeeb464/Joblead.git
- cd <project_folder>

2. Create a `.env` file and set the variables:

```env
DJANGO_SECRET_KEY=super-secret-dev-key
DJANGO_DEBUG=true
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
USE_SQLITE=False
DATABASE_URL=postgres://postgres:postgres@db:5432/postgres
```

Running the Project
- Build and start containers:
```env

docker-compose up --build
```

- Stop containers:
```env  
docker-compose down
```
## using Local environment 
4. Create virtual environment:
``` env
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

Install dependencies:
pip install -r requirements.txt

create .env file 
set the variable keys 
DJANGO_SECRET_KEY=super-secret-dev-key
DJANGO_DEBUG=true
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
USE_SQLITE=True

make sure to set to use sqlite 
USE_SQLITE=True

Apply migrations:
python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser

python manage.py runserver


```
## API Endpoints
- Authentication (JWT)
```env 
POST /api/token/ – Obtain access and refresh tokens.

POST /api/token/refresh/ – Refresh access token.
```
- Users
```env 
GET /api/users/ – List users (Admin only)

POST /api/users/ – Create user

PATCH /api/users/{id}/ – Update user

DELETE /api/users/{id}/ – Delete user
```

- Equipment
```env 
GET /api/equipment/ – List equipment

POST /api/equipment/ – Create equipment

PATCH /api/equipment/{id}/ – Update equipment

DELETE /api/equipment/{id}/ – Delete equipment
```

- Jobs & Tasks
```env 
GET /api/jobs/ – List jobs

POST /api/jobs/ – Create job with nested tasks

PATCH /api/jobs/{id}/ – Update job (only assigned technician or Admin)

GET /api/tasks/ – List tasks

POST /api/tasks/ – Create task

PATCH /api/tasks/{id}/ – Update task (only assigned technician or Admin)
```
```env 
Technician Dashboard

GET /api/technician-dashboard/ – Returns tasks grouped by scheduled date for the logged-in technician.

Audit Logs (Admin Only)

GET /api/audit-logs/ – List all audit logs.

```
```env
Filtering
Jobs and tasks support filtering via query parameters:

GET /api/jobs/?status=Pending&assigned_to=2
GET /api/jobs/?min_date=2025-09-01&max_date=2025-09-30
GET /api/tasks/?status=InProgress&job=1
```






### Postman Collection

A Postman collection is provided for testing all endpoints including authentication, jobs, tasks, equipment, technician dashboard, and audit logs.

- Set base_url and token variables in Postman before testing.

### Notes

- All endpoints require JWT authentication.

- Nested task creation is supported via tasks field in JobSerializer.

- Many-to-many relations (equipment) are assigned using required_equipment_ids in the payload.

- Audit logs automatically track changes for jobs and tasks.