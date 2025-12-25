from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4

# --- 1. Modèles de données (Validation) ---
class TaskInput(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class Task(TaskInput):
    id: str

# --- 2. Initialisation de l'App et "Base de données" ---
app = FastAPI(title="My DevOps API", version="1.0.0")

# Simule une DB en mémoire
fake_db: List[Task] = []

# --- 3. Routes (Logique métier) ---

@app.get("/")
def read_root():
    """Point d'entrée de l'API."""
    return {
        "message": "Welcome to the DevOps API",
        "status": "running",
        "total_tasks": len(fake_db)
    }

@app.get("/health")
def health_check():
    """Vérifie la santé de l'application."""
    return {"status": "ok"}

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    """Récupère toutes les tâches."""
    return fake_db

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task_in: TaskInput):
    """Crée une nouvelle tâche."""
    new_task = Task(
        id=str(uuid4()),
        title=task_in.title,
        description=task_in.description,
        completed=task_in.completed
    )
    fake_db.append(new_task)
    return new_task

@app.get("/tasks/{task_id}", response_model=Task)
def get_task_by_id(task_id: str):
    """Récupère une tâche par son ID."""
    for task in fake_db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")