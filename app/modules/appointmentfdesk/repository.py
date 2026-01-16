from sqlalchemy import text
from app.extensions.db import SessionLocal

class FrontDeskAppointmentRepository:

    @staticmethod
    def confirm_appointment(appointment_id):
        session = SessionLocal()
        try:
            # 1️⃣ Check appointment existence & status
            status_query = text("""
                SELECT status
                FROM appointments
                WHERE appointment_id = :appointment_id
            """)

            result = session.execute(
                status_query,
                {"appointment_id": appointment_id}
            ).fetchone()

            if not result:
                return "NOT_FOUND"

            if result.status == "CONFIRMED":
                return "ALREADY_CONFIRMED"

            # 2️⃣ Update appointment status
            update_query = text("""
                UPDATE appointments
                SET status = 'CONFIRMED',
                    updated_at = NOW()
                WHERE appointment_id = :appointment_id
            """)

            session.execute(update_query, {"appointment_id": appointment_id})
            session.commit()

            return "CONFIRMED"

        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
