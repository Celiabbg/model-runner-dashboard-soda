import time
import random
import threading
from sqlalchemy.orm import Session
from .storage import update_run, save_results

def _simulate_rows(inputs):
    rows = []
    total = 20

    region = inputs.get("region")            # e.g. "APAC"
    year   = inputs.get("year")              # e.g. 2022
    pset   = (inputs.get("parameter_set") or "").lower()  # baseline/optimistic/pessimistic

    # 用 parameter_set 粗略影响 value 的分布
    bias = {"baseline": 1.0, "optimistic": 1.2, "pessimistic": 0.8}.get(pset, 1.0)

    for _ in range(total):
        rows.append({
            "region": region or random.choice(["NA", "EU", "APAC"]),
            "year": year or random.choice([2022, 2023, 2024, 2025]),
            "kpi": random.choice(["revenue", "cost", "margin"]),
            "value": round(random.uniform(1e3, 1e5) * bias, 2),
        })
    return rows

def _summarize(rows):
    s = {"rows": len(rows), "avg_value": round(sum(r["value"] for r in rows)/len(rows), 2)}
    return s

def run_async(db_session_factory, run_id: str, inputs: dict):
    def work():
        db = db_session_factory()
        try:
            for p in range(0, 101, 10):
                update_run(db, run_id, progress=p, status="running", message=f"Processing step {p//10}/10")
                time.sleep(0.6)

            rows = _simulate_rows(inputs)  
            summary = _summarize(rows)
            save_results(db, run_id, summary, rows)
            update_run(db, run_id, status="succeeded", progress=100, message="Completed")
        except Exception as e:
            update_run(db, run_id, status="failed", message=str(e))
        finally:
            db.close()
    threading.Thread(target=work, daemon=True).start()
