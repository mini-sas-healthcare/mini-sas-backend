import os

class BaseConfig:
    ENV = os.getenv("FLASK_ENV", "development")
    DATABASE_URL = os.getenv("DATABASE_URL")
    DEBUG = False
