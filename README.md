# Internship Management System – Django

A web-based internship management platform developed with **Django**, designed to manage the entire internship lifecycle involving **administrators**, **supervisors (encadrants)**, and **interns (stagiaires)**.

The application centralizes internship requests, subject management, evaluations, and document handling within a secure and role-based system.

---

## Features

### Authentication & Roles
- Custom user model with email-based authentication
- Role-based access:
  - Administrator
  - Supervisor (Encadrant)
  - Intern (Stagiaire)
- Login, registration, and logout
- Default password assignment for newly created users (admin-controlled)

---

### Administrator Features
- Admin dashboard
- Manage interns (add, update, delete)
- Manage supervisors (add, update, delete)
- View and manage internship requests
- Change internship request status (accepted / rejected / pending)
- View uploaded documents (reports, attestations)
- Submit internship attestations
- Evaluate interns and assign grades
- Manage personal profile

---

### Supervisor (Encadrant) Features
- Supervisor dashboard
- Propose internship subjects
- Update or delete proposed subjects
- View assigned interns
- Evaluate interns
- Track internship progress
- Manage personal profile

---

### Intern (Stagiaire) Features
- Intern dashboard
- View available internship subjects
- Submit internship requests
- Upload required documents
- Track request status
- Submit internship reports
- View assigned subject and supervisor
- Manage personal profile

---

## Internship Workflow
1. Supervisor proposes internship subjects
2. Intern submits an internship request
3. Administrator reviews and validates/rejects the request
4. Internship is monitored
5. Supervisor evaluates the intern
6. Administrator uploads attestation and final evaluation

---

## Technologies Used

### Backend
- Python
- Django
- Django Authentication (Custom User Model)
- Django Forms
- SQLite 
- File upload management
- Role-based access control

### Frontend
- Django Templates (HTML)
- CSS

---
## Main URL Endpoints

- `/admin_dashboard/` – Admin dashboard
- `/encadrant_dashboard/` – Supervisor dashboard
- `/stagiaire_dashboard/` – Intern dashboard
- `/login/` – Login page
- `/register/` – Intern registration
- `/demande_stage/` – Internship request
- `/gestion_demandes/` – Request management
- `/proposer_sujet/` – Propose subject
- `/mettre_rapport/<id>/` – Upload report

---

## How to Run the Project

1. Clone the repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

3. Install dependencies
pip install -r requirements.txt

4. Apply migrations
python manage.py migrate

5. Run the server
python manage.py runserver

Access the application at:
http://127.0.0.1:8000/

### Author
Abir Ouelhazi

