# Employee Management API

This project is a FastAPI-based employee management system that allows you to create, read, update, patch, and delete employee records.

The API is implemented in [app/main.py](app/main.py) and [employee_routers/routers.py](employee_routers/routers.py), with the database models and schemas defined in [app/models.py](app/models.py), [app/database.py](app/database.py), and [app/schemas.py](app/schemas.py).

## Features

- Create a new employee
- Fetch all employees
- Fetch a single employee by ID
- Update an employee using `PUT`
- Partially update an employee using `PATCH`
- Delete an employee
- Health check endpoint
- Duplicate email protection

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn
- PostgreSQL / SQLite-compatible SQLAlchemy setup

## Project Structure

- [app/main.py](app/main.py) – API app setup and root endpoints
- [app/database.py](app/database.py) – database connection and session setup
- [app/models.py](app/models.py) – Employee ORM model
- [app/schemas.py](app/schemas.py) – request and response validation models
- [app/crud.py](app/crud.py) – business logic for employee operations
- [employee_routers/routers.py](employee_routers/routers.py) – all employee routes
- [requirements.txt](requirements.txt) – Python dependencies

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your database URL:

```env
DATABASE_URL=sqlite:///./employees.db
```

You may also use a PostgreSQL URL if preferred:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/employee_db
```

4. Start the application:

```bash
python -m uvicorn app.main:app --reload
```

5. Open API documentation:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API Endpoints

### 1) Root Endpoint

- Method: `GET`
- URL: `/`
- Description: Confirms the API is running

Example:

```bash
curl http://127.0.0.1:8000/
```

Response:

```json
{
  "message": "Employee Management API is running"
}
```

### 2) Health Check

- Method: `GET`
- URL: `/health`
- Description: Checks service health

Example:

```bash
curl http://127.0.0.1:8000/health
```

Response:

```json
{
  "status": "healthy"
}
```

### 3) Create Employee

- Method: `POST`
- URL: `/employees/`
- Status: `201 Created`
- Description: Adds a new employee record

Request body:

```json
{
  "name": "Ajay Kumar",
  "email": "ajay.kumar@example.com",
  "department": "Engineering",
  "salary": 75000,
  "designation": "Software Engineer"
}
```

Example:

```bash
curl -X POST "http://127.0.0.1:8000/employees/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ajay Kumar",
    "email": "ajay.kumar@example.com",
    "department": "Engineering",
    "salary": 75000,
    "designation": "Software Engineer"
  }'
```

Possible response:

```json
{
  "id": 1,
  "name": "Ajay Kumar",
  "email": "ajay.kumar@example.com",
  "department": "Engineering",
  "salary": 75000,
  "designation": "Software Engineer"
}
```

If the email already exists, the API returns:

```json
{
  "detail": "Email already exists"
}
```

### 4) Get All Employees

- Method: `GET`
- URL: `/employees/`
- Description: Returns all employee records

Example:

```bash
curl http://127.0.0.1:8000/employees/
```

Response:

```json
[
  {
    "id": 1,
    "name": "Ajay Kumar",
    "email": "ajay.kumar@example.com",
    "department": "Engineering",
    "salary": 75000,
    "designation": "Software Engineer"
  }
]
```

### 5) Get Employee by ID

- Method: `GET`
- URL: `/employees/{employee_id}`
- Description: Fetch one employee by its ID

Example:

```bash
curl http://127.0.0.1:8000/employees/1
```

Response:

```json
{
  "id": 1,
  "name": "Ajay Kumar",
  "email": "ajay.kumar@example.com",
  "department": "Engineering",
  "salary": 75000,
  "designation": "Software Engineer"
}
```

If not found:

```json
{
  "detail": "Employee not found"
}
```

### 6) Update Employee (PUT)

- Method: `PUT`
- URL: `/employees/{employee_id}`
- Description: Replaces the full employee record

Request body:

```json
{
  "name": "Ajay K",
  "email": "ajay.k@company.com",
  "department": "Operations",
  "salary": 80000,
  "designation": "Team Lead"
}
```

Example:

```bash
curl -X PUT "http://127.0.0.1:8000/employees/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ajay K",
    "email": "ajay.k@company.com",
    "department": "Operations",
    "salary": 80000,
    "designation": "Team Lead"
  }'
```

### 7) Partial Update Employee (PATCH)

- Method: `PATCH`
- URL: `/employees/{employee_id}`
- Description: Updates one or more fields without replacing the whole record

Request body:

```json
{
  "salary": 85000,
  "designation": "Senior Team Lead"
}
```

Example:

```bash
curl -X PATCH "http://127.0.0.1:8000/employees/1" \
  -H "Content-Type: application/json" \
  -d '{
    "salary": 85000,
    "designation": "Senior Team Lead"
  }'
```

### 8) Delete Employee

- Method: `DELETE`
- URL: `/employees/{employee_id}`
- Description: Deletes an employee record

Example:

```bash
curl -X DELETE "http://127.0.0.1:8000/employees/1"
```

Success response:

```json
{
  "message": "Employee deleted successfully"
}
```

If the record does not exist:

```json
{
  "detail": "Employee not found"
}
```

## API Validation Rules

Employee fields must follow these validation rules:

- `name`: minimum 2 characters
- `email`: valid email format
- `department`: minimum 2 characters
- `salary`: must be greater than 0
- `designation`: minimum 2 characters

## Error Handling

This project returns common HTTP errors such as:

- `200 OK` for successful reads and updates
- `201 Created` for successful employee creation
- `404 Not Found` when an employee does not exist
- `409 Conflict` when an email already exists
- `422 Unprocessable Entity` for invalid request fields

## Manual Testing Notes

This project currently uses manual API testing through FastAPI Swagger UI and `curl` requests rather than an automated `pytest` suite. The recommended way to validate the API is:

1. Run the server with Uvicorn.
2. Open http://127.0.0.1:8000/docs
3. Test each endpoint using the built-in Swagger interface.
4. Use `curl` commands for quick validation from the terminal.

## Example Full Flow

```bash
curl -X POST "http://127.0.0.1:8000/employees/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Rahul Sharma",
    "email": "rahul.sharma@example.com",
    "department": "HR",
    "salary": 60000,
    "designation": "HR Executive"
  }'

curl http://127.0.0.1:8000/employees/

curl http://127.0.0.1:8000/employees/1

curl -X PATCH "http://127.0.0.1:8000/employees/1" \
  -H "Content-Type: application/json" \
  -d '{
    "designation": "Senior HR Executive"
  }'

curl -X DELETE "http://127.0.0.1:8000/employees/1"
```

## License

This project is for educational and internal use.
