from sqlalchemy.orm import Session
from .models import Model, Run, RunResult

def seed_models(db: Session):
    if not db.query(Model).first():
        models = [
            Model(id="linear_reg", name="Linear Regression", params={"alpha": [0.1, 1.0, 10.0]}),
            Model(id="xgb_forecast", name="XGBoost Forecast", params={"max_depth": [3,5,7]}),
            Model(id="simulator", name="Monte Carlo Simulator", params={"trials": [100, 1000, 10000]})
        ]
        db.add_all(models)
        db.commit()

def create_run(db: Session, run: Run):
    db.add(run)
    db.commit()
    db.refresh(run)
    return run

def update_run(db: Session, run_id: str, **kwargs):
    run = db.query(Run).filter(Run.id == run_id).first()
    if not run:
        return None
    for k,v in kwargs.items():
        setattr(run, k, v)
    db.commit()
    db.refresh(run)
    return run

def get_run(db: Session, run_id: str):
    return db.query(Run).filter(Run.id == run_id).first()

def save_results(db: Session, run_id: str, summary, rows):
    rr = RunResult(run_id=run_id, summary=summary, rows=rows)
    db.add(rr)
    db.commit()
    return rr

def get_results(db: Session, run_id: str):
<<<<<<< HEAD
    return db.query(RunResult).filter(RunResult.run_id == run_id).first()
=======
    return db.query(RunResult).filter(RunResult.run_id == run_id).first()
>>>>>>> 09c3099 (Update backend logic)
