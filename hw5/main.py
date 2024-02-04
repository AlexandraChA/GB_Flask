from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

tasks = [{'id':1, 'title':'cleaning', 'desc':'cleaning the flat and do laundry', 'status':True},
         {'id':2, 'title':'dog', 'desc':'walking the dog', 'status':False}]

class Task(BaseModel):
    id:int
    title:str
    desc:str
    status:bool

@app.get("/tasks")
async def get_tasks():
    return tasks

@app.get("/tasks/{id}")
async def get_task_by_id(id):
    needed_task = None
    for task in tasks:
        if task["id"] == int(id):
            needed_task = task
    if needed_task == None:        
        return "Task with that id was not found"
    else:
        return needed_task
    
@app.post("/tasks")
async def create_task(task):
    tasks.append(eval(task))
    return "Task was created"

@app.put("/tasks/{id}")
async def update_task(id, new_task):
    needed_task = None
    for task in tasks:
        if task["id"] == int(id):
            task.update(eval(new_task))
            needed_task = task
    if needed_task == None:
        return "Task with that id was not found"
    else:
        return "This task was updated"

@app.delete("/tasks/{id}")
async def delete_task(id):
    needed_task = None
    for task in tasks:
        if task["id"] == int(id):
            tasks.remove(task)
            needed_task = task
    if needed_task == None:
        return "Task with that id was not found"
    else:
        return "This task was deleted"

#python -m uvicorn main:app --reload