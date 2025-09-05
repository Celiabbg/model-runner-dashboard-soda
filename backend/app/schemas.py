from pydantic import BaseModel
from typing import Any, Dict, List, Optional

class RunCreate(BaseModel):
    model_id: str
    inputs: Dict[str, Any]

class RunStatus(BaseModel):
    run_id: str
    status: str
    progress: int
    message: Optional[str] = None

class RunResults(BaseModel):
    run_id: str
    summary: Dict[str, float]
    rows: List[Dict[str, Any]]