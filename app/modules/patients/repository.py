from sqlalchemy import text
from app.extensions.db import SessionLocal

class PatientRepository:

    @staticmethod
    def get_patient_by_id(patient_id):
        session = SessionLocal()
        try:
            query = text("""
                SELECT
                    patient_id,
                    full_name,
                    phone_number,
                    email,
                    is_verified,
                    created_at
                FROM patients
                WHERE patient_id = :patient_id
            """)

            result = session.execute(
                query,
                {"patient_id": patient_id}
            ).fetchone()

            if not result:
                return None

            return {
                "patient_id": result.patient_id,
                "full_name": result.full_name,
                "phone_number": result.phone_number,
                "email": result.email,
                "is_verified": result.is_verified,
                "created_at": result.created_at.isoformat() if result.created_at else None
            }

        finally:
            session.close()
