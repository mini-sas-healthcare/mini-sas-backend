import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 1. Get the URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Create the Engine
# Note: If using Postgres, ensure the URL starts with postgresql://
engine = create_engine(DATABASE_URL)

# 3. Create the Session factory and BIND it to the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db(app):
    """Optional: Verify connection on app startup"""
    try:
        with engine.connect() as connection:
            print("Successfully connected to the database")
    except Exception as e:
        print(f"Database connection failed: {e}")