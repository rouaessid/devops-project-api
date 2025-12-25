from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from uuid import uuid4

import firebase_admin
from firebase_admin import credentials, firestore

# ============================
# Firebase Initialization
# ============================

cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# ============================
# FastAPI App
# ============================

app = FastAPI(
    title="My DevOps API",
    version="1.0.0",
    description="FastAPI CRUD with Firebase Firestore"
)

# ============================
# Pydantic Models
# ============================

class TaskInput(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class Task(TaskInput):
    id: str

# ============================
# Root & Health
# ============================

@app.get("/")
def root():
    return {
        "message": "Welcome to the DevOps API",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}

# ============================
# CRUD - TASKS
# ============================

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskInput):
    task_id = str(uuid4())
    db.collection("tasks").document(task_id).set(task.dict())
    return Task(id=task_id, **task.dict())

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    tasks = []
    for doc in db.collection("tasks").stream():
        tasks.append(Task(id=doc.id, **doc.to_dict()))
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: str):
    doc = db.collection("tasks").document(task_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Task not found")
    return Task(id=doc.id, **doc.to_dict())

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, task: TaskInput):
    ref = db.collection("tasks").document(task_id)
    if not ref.get().exists:
        raise HTTPException(status_code=404, detail="Task not found")
    ref.update(task.dict())
    return Task(id=task_id, **task.dict())

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: str):
    ref = db.collection("tasks").document(task_id)
    if not ref.get().exists:
        raise HTTPException(status_code=404, detail="Task not found")
    ref.delete()
