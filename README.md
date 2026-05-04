# FastAPI Todo API

A simple REST API built with FastAPI to manage tasks using CRUD operations, SQLite persistence, and basic route protection with a token header.

## Features

- Create a task
- Get all tasks
- Get one task by ID
- Update a task
- Delete a task
- SQLite database persistence
- Basic route protection using a `token` header
- Automatic Swagger documentation

## Tech Stack

- Python
- FastAPI
- SQLite
- Uvicorn

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn
```

Run the project
uvicorn main:app --reload

API available at:

http://127.0.0.1:8000

Swagger documentation:

http://127.0.0.1:8000/docs

Authentication

Protected routes require this header:

token: secret
Example POST request

Endpoint:

POST /tasks

Body:

{
"title": "Learn FastAPI",
"description": "Build a simple backend API",
"completed": false
}

Example response
JSON
{
"message": "Task created"
}
Endpoints
Method Route Description
GET / API health check
GET /tasks Get all tasks
POST /tasks Create a task
GET /tasks/{task_id} Get one task
PUT /tasks/{task_id} Update a task
DELETE /tasks/{task_id} Delete a task
Project purpose

This project was created to strengthen my backend skills in Python, API design, route protection, and data persistence with SQLite.
