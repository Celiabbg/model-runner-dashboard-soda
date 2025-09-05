from sqlalchemy import Column, String, Integer, Float, JSON, Text
from .db import Base

class Model(Base):
    __tablename__ = "models"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    params = Column(JSON, nullable=True)

class Run(Base):
    __tablename__ = "runs"
    id = Column(String, primary_key=True)
    model_id = Column(String, nullable=False)
    status = Column(String, nullable=False)
    progress = Column(Integer, default=0)
    message = Column(Text, nullable=True)

class RunResult(Base):
    __tablename__ = "run_results"
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String, index=True, nullable=False)
    # store simple aggregates as JSON
    summary = Column(JSON, nullable=True)
    # store rows as JSON (small datasets for demo)
    rows = Column(JSON, nullable=True)