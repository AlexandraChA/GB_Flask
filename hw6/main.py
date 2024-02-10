from fastapi import FastAPI
from pydantic import BaseModel, Field
import databases
import sqlalchemy

app = FastAPI()

DATABASE_URL = "sqlite:///mydatabase.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

tasks = sqlalchemy.Table(
    "tasks",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer,
    primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(32)),
    sqlalchemy.Column("desc", sqlalchemy.String(128)),
    sqlalchemy.Column("status", sqlalchemy.Boolean()),
)

@app.get("/fake_tasks/{count}")
async def create_note(count: int):
    for i in range(count):
        query = tasks.insert().values(title=f'Title_{i}',
        desc=f'Desc_{i}', status = False)
        await database.execute(query)
    return {'message': f'{count} fake tasks were created'}

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)

# @app.lifespan("startup")
# async def startup():
#     await database.connect()
# @app.lifespan("shutdown")
# async def shutdown():
#     await database.disconnect()


class Task(BaseModel):
    id:int = Field(title="ID")
    title:str = Field(title="Task title", max_length=50)
    desc:str = Field(title="Task description", max_length=100)
    status:bool = Field(title="Task status", default=False)

class TaskIn(BaseModel):
    title:str = Field(title="Task title", max_length=50)
    desc:str = Field(title="Task description", max_length=100)
    status:bool = Field(title="Task status", default=False)

@app.get("/tasks", response_model=list[Task])
async def get_tasks():
    query = tasks.select()
    return await database.fetch_all(query)

@app.get("/tasks/{id}", response_model=Task)
async def get_task_by_id(id):
    query = tasks.select().where(tasks.c.id == id)
    return await database.fetch_one(query)

    
@app.post("/tasks", response_model=Task)
async def create_task(task: TaskIn):
    query = tasks.insert().values(title=task.title,
desc=task.desc, status = task.status)
    last_record_id = await database.execute(query)
    return {**task.model_dump(), "id": last_record_id}

@app.put("/tasks/{id}", response_model=Task)
async def update_task(id:int, new_task: TaskIn):
    query = tasks.update().where(tasks.c.id ==
    id).values(**new_task.model_dump())
    await database.execute(query)
    return {**new_task.model_dump(), "id": id}

@app.delete("/tasks/{id}")
async def delete_task(id):
    query = tasks.delete().where(tasks.c.id == id)
    await database.execute(query)
    return {'message': 'User was deleted'}

#python -m uvicorn main:app --reload