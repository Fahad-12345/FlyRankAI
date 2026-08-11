from fastapi import FastAPI,status
from fastapi.responses import JSONResponse
app = FastAPI()
task_list = [{"id":1,"title":"task1","done":True},{"id":2,"title":"task2","done":False},{"id":3,"title":"task3","done":False}]
@app.get("/tasks")
def get_tasks():
    return task_list

@app.get("/tasks/{task_id}")
def get_task(task_id:int):
    for task in task_list:
        if task["id"] == task_id:
            return task
    return JSONResponse(status_code=404,content = {"error": f"Task {task_id} not found"})
@app.get("/")
async def root():
    apiDictionary = {
        "name":"Task API",
        "version":"1.0",
        "endpoints":["/tasks"]
    }
    return apiDictionary
# health endpoint
@app.get("/health")
async def health():
    return{"status":"ok"}
