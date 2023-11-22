import os
import datetime
from dotenv import load_dotenv
from typing import Optional, Annotated

import uvicorn
from fastapi import FastAPI, Request, Body, Form
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from jinja_filters import num2int, status_text, user_created_str

from models import Task
from helpers import create_task
from contextlib import asynccontextmanager

from mgutils import call_magic

load_dotenv()

sqlite_filename = os.environ.get('SQLITE_FILENAME')
sqlite_url = f"sqlite:///{sqlite_filename}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    # code to execute when app is loading
    create_db_and_tables()
    yield
    # code to execute when app is shutting down


app = FastAPI(lifespan=app_lifespan)

app.mount("/static", StaticFiles(directory="../static"), name="static")

templates = Jinja2Templates(directory="templates", 
    trim_blocks = True, lstrip_blocks = True, autoescape = True)
templates.env.filters["num2int"] = num2int
templates.env.filters["status_text"] = status_text
templates.env.filters["user_created_str"] = user_created_str


'''
# deprecated
@app.on_event("startup")
async def on_startup():
    create_db_and_tables()
'''


@app.get("/tasks/")
def read_tasks():
    with Session(engine) as session:
        tasks = session.exec(select(Task)).all()
        return tasks


@app.get("/tasklist/", response_class=HTMLResponse)
async def get_tasklist(request: Request):
    with Session(engine) as session:
        tasks = session.exec(select(Task)).all()

    return templates.TemplateResponse("tasks.html", {"request": request, "tasks": tasks})


def build_page(request: Request):
    list_names = ["To Do", "In Progress", "Done"]

    with Session(engine) as session:
        tasks = session.exec(select(Task)).all()

    return templates.TemplateResponse("kanban.html",
        {"request": request, "tasks": tasks, "list_names": list_names})


def build_list(request: Request, status: int):
    with Session(engine) as session:
        tasks = session.exec(select(Task).where(Task.status == status)).all()

    return templates.TemplateResponse("kanban-list.html",
        {"request": request, "tasks": tasks, "status": status})


def build_task(request: Request, task: Task):

    return templates.TemplateResponse("task-card.html",
        {"request": request, "task": task})


@app.post("/kanban/", response_class=HTMLResponse)
async def k_post(request:Request, 
    task_name: Annotated[str, Form()], 
    description: Annotated[str, Form()],
    task_status: Annotated[int, Form()]):
    
    task = create_task(task_name, description, task_status, 'User')
    
    with Session(engine) as session:
        session.add(task)
        session.commit()
        session.refresh(task)

    return build_task(request, task)


@app.post("/kanban/{id}", response_class=HTMLResponse)
def k_post_update(request:Request, id: int, 
    task_name: Annotated[str, Form()], 
    description: Annotated[str, Form()]):

    try:
        with Session(engine) as session:
            statement = select(Task).where(Task.id == id)  
            results = session.exec(statement)  
            task = results.one()  

            task.task_name = task_name
            task.description = description
            task.updated_by = 'User'
            task.updated_date = str(datetime.datetime.now())

            session.add(task)  
            session.commit()      
            session.refresh(task)
    except:
        pass
    
    return build_page(request)


@app.get("/kanban/", response_class=HTMLResponse)
async def kanban(request: Request):

    return build_page(request)


@app.delete("/kanban/{id}", response_class=HTMLResponse)
async def k_delete(request:Request, id: int):

    status = 0
    try:
        with Session(engine) as session:
            statement = select(Task).where(Task.id == id)  
            results = session.exec(statement)  
            task = results.one()  
            status = task.status
            session.delete(task)  
            session.commit()      
    except:
        pass

    #return build_list(request, status)
    return b''


@app.post("/kanban/move/", response_class=HTMLResponse)
async def k_move(request:Request,  
    id: Annotated[int, Form()], 
    from_list: Annotated[str, Form()], 
    old_index: Annotated[int, Form()],
    to_list: Annotated[str, Form()], 
    new_index: Annotated[int, Form()]):

    try:
        with Session(engine) as session:
            statement = select(Task).where(Task.id == id)  
            results = session.exec(statement)  
            task = results.one()  
            task.status = to_list
            #task.updated_by = 'User'
            #task.updated_date = str(datetime.datetime.now())
            session.add(task)  
            session.commit()      
            session.refresh(task)
    except:
        pass

    return build_task(request, task)


@app.get("/kanban/edit/{id}", response_class=HTMLResponse)
def k_edit_card(request:Request, id: int):
    try:
        with Session(engine) as session:
            statement = select(Task).where(Task.id == id)  
            results = session.exec(statement)  
            task = results.one()  

    except:
        pass

    return templates.TemplateResponse("edit-task-dialog.html",
    {"request": request, "task": task})


@app.get("/kanban/list/{status}", response_class=HTMLResponse)
def k_get_list(request:Request, status: int):
    
    return build_list(request, status)


# Magic Wrappers

@app.get("/magic/", response_class=HTMLResponse)
def magic_kanban():
    return 'Hello, World! from Magic'


@app.get("/magic/hello", response_class=HTMLResponse)
def magic_hello():
    return call_magic(appname = 'mg-sue', prgname = 'HelloWorld')


@app.get("/magic/tasks", response_class=HTMLResponse)
def magic_tasks():
    return call_magic(appname = 'mg-sue', prgname = 'Tasks')


@app.get("/magic/kanban", response_class=HTMLResponse)
def magic_kanban():
    return call_magic(appname = 'mg-sue', prgname = 'Kanban')
    

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")