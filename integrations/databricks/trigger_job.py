import os, requests

DATABRICKS_HOST = os.environ.get("DATABRICKS_HOST", "https://<workspace>.azuredatabricks.net")
DATABRICKS_TOKEN = os.environ.get("DATABRICKS_TOKEN", "<token>")
JOB_ID = os.environ.get("DATABRICKS_JOB_ID", "<job_id>")

def trigger(params: dict):
    url = f"{DATABRICKS_HOST}/api/2.1/jobs/run-now"
    headers = {"Authorization": f"Bearer {DATABRICKS_TOKEN}"}
    payload = {"job_id": JOB_ID, "notebook_params": params}
    r = requests.post(url, headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    data = r.json()
    return data["run_id"]

def get_status(run_id: int):
    url = f"{DATABRICKS_HOST}/api/2.1/jobs/runs/get?run_id={run_id}"
    headers = {"Authorization": f"Bearer {DATABRICKS_TOKEN}"}
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()