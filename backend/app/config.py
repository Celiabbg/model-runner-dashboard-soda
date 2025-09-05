import os

APP_ENV = os.environ.get("APP_ENV", "dev")
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./data/app.db")