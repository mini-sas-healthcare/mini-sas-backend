from app.extensions.db import SessionLocal

class AppointmentRepository:

    @staticmethod
    def create():
        session = SessionLocal()
        try:
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
