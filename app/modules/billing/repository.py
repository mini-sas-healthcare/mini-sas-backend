from sqlalchemy import text
from app.extensions.db import SessionLocal

class FrontDeskBillingRepository:

    @staticmethod
    def complete_billing(appointment_id):
        session = SessionLocal()
        try:
            # 1️⃣ Check billing existence & status
            status_query = text("""
                SELECT status
                FROM appointment_billing
                WHERE appointment_id = :appointment_id
            """)

            result = session.execute(
                status_query,
                {"appointment_id": appointment_id}
            ).fetchone()

            if not result:
                return "NOT_FOUND"

            if result.status == "COMPLETED":
                return "ALREADY_COMPLETED"

            # 2️⃣ Update billing status
            update_query = text("""
                UPDATE appointment_billing
                SET status = 'COMPLETED',
                    updated_at = NOW()
                WHERE appointment_id = :appointment_id
            """)

            session.execute(update_query, {"appointment_id": appointment_id})
            session.commit()

            return "COMPLETED"

        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
