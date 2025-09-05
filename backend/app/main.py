from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from uuid import uuid4

from .db import Base, engine, SessionLocal
from .models import Model, Run
from .schemas import RunCreate, RunStatus, RunResults
from .storage import seed_models, create_run, get_run, get_results
from .runner import run_async

app = FastAPI(title="Model Runner API", version="1.0.0")

# CORS (dev-friendly)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB init
Base.metadata.create_all(bind=engine)
with SessionLocal() as db:
    seed_models(db)

@app.get("/api/models")
def list_models():
    with SessionLocal() as db:
        models = db.query(Model).all()
        return {"models": [{"id": m.id, "name": m.name, "params": m.params or {}} for m in models]}

@app.post("/api/runs")
def create_run_endpoint(payload: RunCreate):
    run_id = str(uuid4())
    run = Run(id=run_id, model_id=payload.model_id, status="queued", progress=0, message=None)
    with SessionLocal() as db:
        create_run(db, run)
    # kick background
    run_async(SessionLocal, run_id, payload.inputs)
    return {"run_id": run_id}

@app.get("/api/runs/{run_id}/status", response_model=RunStatus)
def get_run_status(run_id: str):
    with SessionLocal() as db:
        r = get_run(db, run_id)
        if not r:
            raise HTTPException(404, "Run not found")
        return RunStatus(run_id=r.id, status=r.status, progress=r.progress, message=r.message or None)

@app.get("/api/runs/{run_id}/results", response_model=RunResults)
def get_run_results(run_id: str):
    with SessionLocal() as db:
        rr = get_results(db, run_id)
        if not rr:
            raise HTTPException(404, "Results not available yet")
        return RunResults(run_id=run_id, summary=rr.summary or {}, rows=rr.rows or [])