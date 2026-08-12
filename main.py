from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import Any

app = FastAPI()

task_list = [
    {"id": 1, "title": "task1", "done": True},
    {"id": 2, "title": "task2", "done": False},
    {"id": 3, "title": "task3", "done": False}
]


@app.get("/tasks")
def get_tasks():
    return task_list


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in task_list:
        if task["id"] == task_id:
            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )


@app.get("/")
async def root():
    apiDictionary = {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }
    return apiDictionary


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/tasks", status_code=201)
def create_task(data: dict[str, Any]):

    if "title" not in data or not isinstance(data["title"], str) or not data["title"].strip():
        return JSONResponse(
            status_code=400,
            content={"error": "title is required and cannot be empty"}
        )

    new_id = max(t["id"] for t in task_list) + 1

    new_task = {
        "id": new_id,
        "title": data["title"],
        "done": False
    }

    task_list.append(new_task)

    return new_task