from sqlalchemy import text
from app.extensions.db import SessionLocal

class HealthRepository:
    @staticmethod
    def ping_db():
        session = SessionLocal()
        try:
            # SQLAlchemy 2.x requires text()
            session.execute(text("SELECT 1"))
            return True
        except Exception:
            return False
        finally:
            session.close()