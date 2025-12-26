import logging
from pythonjsonlogger import jsonlogger
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, List
from uuid import uuid4
import firebase_admin
from firebase_admin import credentials, firestore
from prometheus_fastapi_instrumentator import Instrumentator
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# --- 1. CONFIGURATION DES LOGS JSON ---
logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

# --- 2. CONFIGURATION TRACING ---
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# --- 3. FIREBASE INIT ---
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-key.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

# --- 4. APP SETUP ---
app = FastAPI(title="My DevOps API", version="1.0.0")

# Instrumenter l'app pour Prometheus (Metrics)
Instrumentator().instrument(app).expose(app)
# Instrumenter l'app pour le Tracing
FastAPIInstrumentor.instrument_app(app)

# --- MODELS ---
class TaskInput(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class Task(TaskInput):
    id: str

# --- ROUTES ---
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Logue chaque requête avec son statut."""
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Request finished: {response.status_code}")
    return response

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskInput):
    task_id = str(uuid4())
    db.collection("tasks").document(task_id).set(task.dict())
    logger.info(f"Task created successfully: {task_id}")
    return Task(id=task_id, **task.dict())

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    tasks = [Task(id=doc.id, **doc.to_dict()) for doc in db.collection("tasks").stream()]
    return tasks

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
