from sqlalchemy import text
from app.extensions.db import SessionLocal
import uuid

class AppointmentRepository:

# doctor side functionality
    @staticmethod
    def create_booking(data):
        """
        Transactional logic for booking:
        1. Mark the slot as unavailable in 'provider_schedule'.
        2. Create a 'PENDING' record in 'appointments'.
        """
        session = SessionLocal()
        try:
            # Step 1: Atomic Update of the Slot
            # We filter by 'is_available = TRUE' to prevent double-booking (Race Condition)
            update_slot = text("""
                UPDATE provider_schedule 
                SET is_available = FALSE 
                WHERE id = :slot_id AND is_available = TRUE
                RETURNING provider_id, slot_time
            """)
            
            slot_result = session.execute(update_slot, {"slot_id": data['slot_id']})
            slot_row = slot_result.fetchone()

            if not slot_row:
                return None  # Slot is already booked or doesn't exist

            # Step 2: Insert into 'appointments' table using your EXACT schema
            # We generate a unique business appointment_id (example format: APT-UUID_PART)
            business_id = f"APT-{str(uuid.uuid4())[:8].upper()}"
            
            insert_appointment = text("""
                INSERT INTO appointments (
                    appointment_id, provider_id, patient_id, 
                    slot_time, status, retry_count
                )
                VALUES (
                    :appointment_id, :provider_id, :patient_id, 
                    :slot_time, 'PENDING', 0
                )
                RETURNING id, appointment_id
            """)
            
            appt_result = session.execute(insert_appointment, {
                "appointment_id": business_id,
                "provider_id": slot_row.provider_id,
                "patient_id": data['patient_id'],
                "slot_time": slot_row.slot_time
            })
            
            new_record = appt_result.fetchone()
            session.commit()
            
            return {
                "internal_id": str(new_record.id),
                "business_id": new_record.appointment_id
            }

        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
            
    @staticmethod
    def get_by_provider(provider_id):
        """Fetch all appointments for a specific doctor"""
        session = SessionLocal()
        try:
            # We select specific columns from your actual appointments schema
            query = text("""
                SELECT appointment_id, patient_id, slot_time, status, retry_count
                FROM appointments 
                WHERE provider_id = :provider_id
                ORDER BY slot_time ASC
            """)
            result = session.execute(query, {"provider_id": provider_id})
            # Convert SQLAlchemy rows to a list of dictionaries for JSON
            return [dict(row._mapping) for row in result]
        finally:
            session.close()

    @staticmethod
    def get_by_provider(provider_id):
        session = SessionLocal()
        try:
            query = text("""
                SELECT appointment_id, patient_id, slot_time, status, retry_count
                FROM appointments 
                WHERE provider_id = :provider_id
                ORDER BY slot_time ASC
            """)
            result = session.execute(query, {"provider_id": provider_id})
            
            # Use a list comprehension to convert datetime objects to strings
            return [
                {
                    "appointment_id": row.appointment_id,
                    "patient_id": row.patient_id,
                    "slot_time": row.slot_time.isoformat(), # FIX: Convert to string
                    "status": row.status,
                    "retry_count": row.retry_count
                } for row in result
            ]
        finally:
            session.close()

    @staticmethod
    def get_all():
        session = SessionLocal()
        try:
            query = text("""
                SELECT appointment_id, provider_id, patient_id, slot_time, status 
                FROM appointments 
                ORDER BY created_at DESC
            """)
            result = session.execute(query)
            
            # FIX: Convert slot_time to isoformat here as well
            return [
                {
                    "appointment_id": row.appointment_id,
                    "provider_id": row.provider_id,
                    "patient_id": row.patient_id,
                    "slot_time": row.slot_time.isoformat(),
                    "status": row.status
                } for row in result
            ]
        finally:
            session.close()
