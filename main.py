from fastapi import FastAPI,Response
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
@app.put("/tasks/{task_id}")
def update_task(task_id: int, data: dict[str, Any]):

    if not data:
        return JSONResponse(
            status_code=400,
            content={"error": "Request body cannot be empty"}
        )

    for task in task_list:

        if task["id"] == task_id:

            if "title" in data:
                if not isinstance(data["title"], str) or not data["title"].strip():
                    return JSONResponse(
                        status_code=400,
                        content={"error": "title must be a non-empty string"}
                    )

                task["title"] = data["title"]

            if "done" in data:
                if not isinstance(data["done"], bool):
                    return JSONResponse(
                        status_code=400,
                        content={"error": "done must be true or false"}
                    )

                task["done"] = data["done"]

            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    for i, task in enumerate(task_list):

        if task["id"] == task_id:
            task_list.pop(i)
            return Response(status_code=204)

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )