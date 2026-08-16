from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import sqlite3

app = FastAPI()

DATABASE = "tasks.db"

class TaskCreate(BaseModel):
    title: str


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Create database and table
def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)

    # Insert example tasks only if table is empty
    count = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]

    if count == 0:
        conn.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            [
                ("task1", 1),
                ("task2", 0),
                ("task3", 0)
            ]
        )

    conn.commit()
    conn.close()


init_db()


@app.get("/tasks")
def get_tasks():
    conn = get_db()

    tasks = conn.execute(
        "SELECT id, title, done FROM tasks"
    ).fetchall()

    conn.close()

    return [dict(task) for task in tasks]

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    conn = get_db()

    task = conn.execute(
        "SELECT id, title, done FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    conn.close()

    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": "Task not found"}
        )

    return dict(task)

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):

    if not task.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required"}
        )

    conn = get_db()

    cursor = conn.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (task.title, 0)
    )

    conn.commit()

    new_id = cursor.lastrowid

    new_task = conn.execute(
        "SELECT id, title, done FROM tasks WHERE id = ?",
        (new_id,)
    ).fetchone()

    conn.close()

    return dict(new_task)