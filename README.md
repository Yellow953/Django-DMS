# Data Management System (Django Backend)

A dynamic schema-driven backend system for managing data schemas, CRUD operations, and bulk CSV imports with secure APIs.

## Features

- **Schema Management**: Define/update tables and fields via API.
- **CRUD Operations**: Create, read, update, and delete data entries.
- **Search & Filter**: Exact/partial matches, sorting, and pagination.
- **Bulk CSV Imports**: Asynchronous processing for 100k+ records.
- **Security**: JWT authentication for all endpoints.

## Tech Stack

- Python 3.12
- Django 5
- PostgreSQL 16
- Celery (with Redis)
- Django REST Framework

## Setup

### Prerequisites

- Python 3.12, PostgreSQL 16, Redis, Docker (optional)

### Installation

1. Clone the repository:
   git clone https://github.com/your-username/data-management-system.git
   cd data-management-system

2. Create a virtual environment:
   python -m venv venv
   source venv/bin/activate # Linux/macOS
   venv\Scripts\activate # Windows

3. Install dependencies:
   pip install -r requirements.txt

4. Configure environment variables (create .env):
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   SECRET_KEY=your-django-secret-key
   CELERY_BROKER_URL=redis://localhost:6379/0
   EMAIL_HOST=your-smtp-host
   EMAIL_PORT=587
   EMAIL_HOST_USER=your-email@example.com
   EMAIL_HOST_PASSWORD=your-email-password

5. Run migrations:
   python manage.py migrate

6. Start the server:
   python manage.py runserver

7. Start Celery (in a new terminal):
   celery -A data_management_system worker --loglevel=info
   Access the admin panel at http://localhost:8000/admin/.

## API Examples

### Authentication

curl -X POST http://localhost:8000/api/token/ \
 -H "Content-Type: application/json" \
 -d '{"username": "admin", "password": "yourpassword"}'

### Create a Schema

curl -X POST http://localhost:8000/api/schemas/ \
 -H "Authorization: Bearer YOUR_JWT_TOKEN" \
 -H "Content-Type: application/json" \
 -d '{"name": "Customer", "fields": [{"name": "email", "field_type": "text", "unique": true}]}'

### Import CSV Data

curl -X POST http://localhost:8000/api/data/1/import/ \
 -H "Authorization: Bearer YOUR_JWT_TOKEN" \
 -F "file=@/path/to/customers.csv"
