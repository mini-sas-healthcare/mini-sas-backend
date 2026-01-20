from sqlalchemy import text
from app.extensions.db import SessionLocal

class FrontDeskAppointmentRepository:

    @staticmethod
    def confirm_appointment(appointment_id, billing_data=None):
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

            # 3️⃣ Optional billing creation (IDEMPOTENT)
            if billing_data:
                billing_exists_query = text("""
                    SELECT 1
                    FROM appointment_billing
                    WHERE appointment_id = :appointment_id
                """)

                billing_exists = session.execute(
                    billing_exists_query,
                    {"appointment_id": appointment_id}
                ).fetchone()

                if not billing_exists:
                    insert_billing_query = text("""
                        INSERT INTO appointment_billing (
                            appointment_id,
                            patient_id,
                            provider_id,
                            cpt_code,
                            payer_code,
                            amount,
                            status,
                            created_at,
                            updated_at
                        )
                        VALUES (
                            :appointment_id,
                            :patient_id,
                            :provider_id,
                            :cpt_code,
                            :payer_code,
                            :amount,
                            'PENDING',
                            NOW(),
                            NOW()
                        )
                    """)

                    session.execute(insert_billing_query, {
                        "appointment_id": appointment_id,
                        "patient_id": billing_data["patient_id"],
                        "provider_id": billing_data["provider_id"],
                        "cpt_code": billing_data["cpt_code"],
                        "payer_code": billing_data["payer_code"],
                        "amount": billing_data["amount"],
                    })

            session.commit()
            return "CONFIRMED"

        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


    @staticmethod
    def get_pending_appointments():
        session = SessionLocal()
        try:
            query = text("""
                SELECT
                    appointment_id,
                    provider_id,
                    patient_id,
                    slot_time,
                    status,
                    created_at,
                    updated_at
                FROM appointments
                WHERE status = 'PENDING'
                ORDER BY created_at ASC
            """)

            rows = session.execute(query).mappings().all()
            [dict(row) for row in rows]

        finally:
            session.close()

    @staticmethod
    def get_todays_appointments():
        session = SessionLocal()
        try:
            query = text("""
                SELECT
                    appointment_id,
                    provider_id,
                    patient_id,
                    slot_time,
                    status,
                    created_at,
                    updated_at
                FROM appointments
                WHERE slot_time >= DATE_TRUNC('day', NOW())
                  AND slot_time < DATE_TRUNC('day', NOW()) + INTERVAL '1 day'
                ORDER BY slot_time ASC
            """)

            rows = session.execute(query).mappings().all()
            [dict(row) for row in rows]

        finally:
            session.close()