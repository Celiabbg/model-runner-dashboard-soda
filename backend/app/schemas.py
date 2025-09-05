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

"""
🎤 演讲解释（精简版）

    这里我定义了三个 数据模型，用来统一接口输入输出格式：

    RunCreate

        用于新建一次运行请求。

        包含：model_id（选择的模型）和 inputs（参数字典）。

    RunStatus

        表示一次运行的状态。

        包含：run_id、当前 status（如 running/failed）、progress（百分比），以及可选的提示信息。

    RunResults

        表示一次运行完成后的结果。

        包含：run_id、summary（统计信息，比如平均值）、rows（结果数据表）。

✨ 总结

“这段代码的作用是：定义了前后端 API 的数据格式，确保接口输入输出结构清晰、可验证。
换句话说，RunCreate 是输入，RunStatus 是过程，RunResults 是输出。”

"""