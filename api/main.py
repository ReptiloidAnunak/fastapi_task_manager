from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from contextlib import asynccontextmanager
from database.models import Task, init_db
from database.database import get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing database...")
    init_db()
    print("Database initialized!")
    yield

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def index(request: Request, db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    print(f"Found {len(tasks)} tasks")
    return templates.TemplateResponse(request, "index.html", {"tasks": tasks})


@app.get("/get-task/{task_id}")
def get_edit_task(task_id: str, request: Request, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        return templates.TemplateResponse(request, "task.html", {"task": task})
    return RedirectResponse(url="/", status_code=303)


@app.post("/update-task/{task_id}")
def update_task(
    task_id: str,
    title: str = Form(...),
    description: str = Form(...),
    status: str = Form(...),
    db: Session = Depends(get_db)
    ):
    print(f"Updating task ID {task_id} with title: {title}, description: {description}, status: {status}")
    
    if title is None or len(title) < 5:
        raise HTTPException(
            status_code=400, 
            detail="Title must be at least 5 characters long"
        )
    elif description is None or len(description) < 5:
        raise HTTPException(
            status_code=400, 
            detail="Description must be at least 5 characters long"
        )
    
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            task.title = title
            task.description = description
            task.status = status
            task.updated_at = datetime.now()
            
            db.commit()
            db.refresh(task)
            
            print(f"Task updated with ID: {task.id}")
        else:
            print(f"Task not found with ID: {task_id}")
        
        return RedirectResponse(url="/", status_code=303)
        
    except Exception as e:
        print(f"Error updating task: {e}")
        db.rollback()
        raise e


@app.post("/create-task")
def create_task(
    title: str = Form(...),
    description: str = Form(...),
    status: str = Form(...),
    db: Session = Depends(get_db)
    ):
    print(f"Creating task: {title}, {description}, {status}")
    
    if title is None or len(title) < 5:
        raise HTTPException(
            status_code=400, 
            detail="Title must be at least 5 characters long"
        )
    elif description is None or len(description) < 5:
        raise HTTPException(
            status_code=400, 
            detail="Desctiption must be at least 5 characters long"
        )

    try:
        task = Task(
            title=title,
            description=description,
            status=status,
            created_at=datetime.now()
        )
        
        db.add(task)
        db.commit()
        db.refresh(task)
        
        print(f"Task created with ID: {task.id}")
        
        return RedirectResponse(url="/", status_code=303)
        
    except Exception as e:
        print(f"Error creating task: {e}")
        db.rollback()
        raise e


@app.get("/delete-task/{task_id}")
def delete_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        print(f"Task deleted with ID: {task.id}")
    else:
        print(f"Task not found with ID: {task_id}")
    return RedirectResponse(url="/", status_code=303)