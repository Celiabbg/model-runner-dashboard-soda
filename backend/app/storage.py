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
    return db.query(RunResult).filter(RunResult.run_id == run_id).first()


"""

🎤 演讲解释（精简版）

这里的代码封装了几组 数据库操作函数，负责和运行记录相关的 CRUD：

seed_models
初始化数据库，如果模型表是空的，就预置几个示例模型（线性回归、XGBoost、模拟器）。

create_run
    建一次运行（Run），存到数据库并返回。

update_run
    根据 run_id 更新运行状态，比如进度、状态、错误信息。

get_run
    查询某个 run 的当前信息。

save_results
    把运行结果（summary 和 rows）保存到 RunResult 表里。

get_results
    查询某个 run 的结果。

✨ 总结

    “简单来说，这些函数就是数据库层的工具方法：

        预置模型

        保存 run 的状态

        存储和查询结果

前端和异步 worker 都是通过它们来读写数据库，从而保持状态一致。”
"""