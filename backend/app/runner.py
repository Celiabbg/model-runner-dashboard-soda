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

    """
    这段代码实现了一个 异步任务模拟器，用来假装运行模型并生成结果。流程是这样的：

    1. 进度更新

        每隔一段时间更新一次数据库里的 run 状态和进度（0% → 100%）。

        前端就能通过 /status API 轮询看到进度条在走。

    2. 生成结果数据

        模拟出一些随机的行数据，比如 region、year、KPI（收入、成本、利润）、以及一个数值。

        根据不同的参数集（baseline / optimistic / pessimistic）调整数值偏差。

    3. 汇总统计

        计算平均值和总行数，形成 summary。

    4. 保存结果

        把详细行和 summary 一起存进数据库，并把 run 标记为完成。

        如果出错，更新为失败状态。

    ✨ 总结

        “简单来说，这段代码就是在后台假装跑一个模型：
        它不断更新进度 → 随机生成一些结果数据 → 汇总统计 → 存进数据库。
        这样前端用户就能看到一个真实的‘长任务’执行过程。”
    """
