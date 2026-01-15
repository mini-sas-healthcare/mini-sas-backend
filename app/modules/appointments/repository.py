from sqlalchemy import text
from app.extensions.db import SessionLocal
import uuid

class AppointmentRepository:
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