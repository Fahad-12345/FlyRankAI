# Task API — SQLite Database

A simple REST API built with FastAPI and SQLite as part of the FlyRank AI Internship Program — Week 3.

This assignment continues the Week 2 CRUD API by replacing the in-memory task list with a persistent SQLite database.

## Overview

In Week 2, tasks were stored in a Python list.

Client → FastAPI → In-Memory Array

In Week 3, the storage layer has been replaced with SQLite.

Client → FastAPI → SQLite Database

The API endpoints remain the same, but task data now survives server restarts.

## Technologies

- Python
- FastAPI
- SQLite
- Uvicorn
- Pydantic

## Project Structure

Week_3/
├── main.py
├── tasks.db
├── README.md
└── screenshots/
    └── sqlite_query.png

## Database

The application uses SQLite with a database file named `tasks.db`.

The database is automatically created when the application starts if it does not already exist.

The `tasks` table is also automatically created if it is missing.

The table contains:

| Column | Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| title | TEXT | Task title |
| done | BOOLEAN | Completion status |

Three example tasks are inserted automatically only when the database is empty.

## Running the Application

Install the required packages:

    pip install fastapi uvicorn

Start the server:

    uvicorn main:app --reload

The API runs at:

    http://localhost:8000

Swagger UI:

    http://localhost:8000/docs

## API Endpoints

### GET /tasks

Returns all tasks from the SQLite database.

Example response:

    [
        {
            "id": 1,
            "title": "task1",
            "done": true
        },
        {
            "id": 2,
            "title": "task2",
            "done": false
        }
    ]

### GET /tasks/{task_id}

Returns a single task by ID.

Example:

    GET /tasks/1

Example response:

    {
        "id": 1,
        "title": "task1",
        "done": true
    }

If the task does not exist:

    {
        "error": "Task not found"
    }

HTTP status: 404 Not Found

### POST /tasks

Creates a new task in the SQLite database.

Request:

    {
        "title": "Buy milk"
    }

Successful response:

    {
        "id": 4,
        "title": "Buy milk",
        "done": false
    }

HTTP status: 201 Created

### PUT /tasks/{task_id}

Updates an existing task.

Request:

    {
        "title": "Buy groceries",
        "done": true
    }

Example response:

    {
        "id": 4,
        "title": "Buy groceries",
        "done": true
    }

If the task does not exist, the API returns 404 Not Found.

### DELETE /tasks/{task_id}

Deletes a task from the SQLite database.

Example:

    DELETE /tasks/4

Successful response:

    204 No Content

## Persistence

The main purpose of this assignment is to demonstrate persistent storage.

A task can be created using `POST /tasks`, after which the server can be stopped and restarted.

Running `GET /tasks` after restarting the server will still return the previously created task.

This is different from Week 2, where all tasks were stored in memory and disappeared when the application restarted.

## SQL Queries

The database was also explored using a SQLite database viewer.

List every task:

    SELECT * FROM tasks;

Show only completed tasks:

    SELECT * FROM tasks WHERE done = 1;

Count all tasks:

    SELECT COUNT(*) FROM tasks;

Mark every task as completed:

    UPDATE tasks SET done = 1;

Delete all completed tasks:

    DELETE FROM tasks WHERE done = 1;

Changes made directly to the database can be verified through the API.

## Error Handling

Unknown task IDs return a 404 response.

Example:

    {
        "error": "Task not found"
    }

Invalid requests are rejected with an appropriate HTTP error response.

## Screenshots

The `screenshots` directory contains evidence of the SQLite database and API testing.

Example:

    screenshots/
    └── database_viewer.png

## Assignment Stages

### Stage 0 — Create SQLite Database

Created the `tasks.db` SQLite database and automatically created the `tasks` table.

Three example tasks are inserted only when the database is empty.

Commit:

    Stage 0: create SQLite database

### Stage 1 — Database Read Endpoints

Updated `GET /tasks` and `GET /tasks/{task_id}` to retrieve tasks from SQLite using SQL queries.

Unknown task IDs return 404.

Commit:

    Stage 1: database read endpoints

### Stage 2 — Insert Into Database

Updated `POST /tasks` to insert new tasks into the SQLite database.

New tasks remain available after restarting the server.

Commit:

    Stage 2: insert into database

### Stage 3 — Update and Delete With SQL

Updated `PUT /tasks/{task_id}` and `DELETE /tasks/{task_id}` to modify and remove records from SQLite.

Commit:

    Stage 3: update and delete with SQL

### Stage 4 — Explored SQLite

Opened the database using a SQLite database viewer and executed SQL queries manually.

Verified that database changes are reflected through the API.

Commit:

    Stage 4: explored SQLite

### Stage 5 — Database Documentation

Updated the README with SQLite information, setup instructions, SQL examples, and database screenshots.

Verified that someone cloning the repository can run the project and automatically create the database.

Commit:

    Stage 5: database documentation

## Requirements Completed

- [x] API exposes the same CRUD endpoints as Week 2
- [x] Tasks are stored in SQLite instead of memory
- [x] Data survives server restarts
- [x] Database is automatically created if missing
- [x] Tasks table is automatically created if missing
- [x] Three example tasks are inserted only on the first run
- [x] CRUD operations use SQL queries
- [x] Unknown IDs return 404
- [x] Invalid requests return appropriate errors
- [x] README updated
- [x] Database screenshot added
- [x] SQLite queries tested manually

## Key Concept

The main concept demonstrated by this assignment is separation between the API layer and the storage layer.

The API remains the same:

    GET /tasks
    POST /tasks
    PUT /tasks/{id}
    DELETE /tasks/{id}

Only the storage implementation changed.

Week 2:

    FastAPI → Python List

Week 3:

    FastAPI → SQLite

This demonstrates that the API can remain stable while the underlying database implementation changes.

## Author

Fahad Irfan

FlyRank AI Internship Program — Week 3