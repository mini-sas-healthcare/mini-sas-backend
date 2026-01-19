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

        Args:
            data (dict): Contains 'slot_id' and 'patient_id'.
        Returns:
            dict: Internal UUID and Business ID of the new appointment.
        """
        session = SessionLocal()
        try:
            # Step 1: Atomic Update of the Slot
            # We filter by 'is_available = TRUE' to prevent double-booking (Race Condition)
            # This ensures that even with high concurrency, one slot = one patient.
            update_slot = text("""
                UPDATE provider_schedule
                SET is_available = FALSE
                WHERE id = :slot_id
                  AND is_available = TRUE
                RETURNING provider_id, slot_time
            """)

            # Attempt to lock the slot; if another request already took it,
            # this query will return no rows.
            slot_result = session.execute(
                update_slot, {"slot_id": data["slot_id"]}
            )
            slot_row = slot_result.fetchone()

            # Logic Check: If no row was updated, the slot was already taken or invalid.
            # Returning None allows the service layer to respond gracefully.
            if not slot_row:
                return None

            # Step 2: Generate Business ID
            # Human-readable ID for tracking (e.g., APT-A1B2C3D4)
            # Shortened UUID is enough for uniqueness while remaining readable.
            business_id = f"APT-{uuid.uuid4().hex[:8].upper()}"

            # Step 3: Insert into 'appointments' table
            # Status defaults to 'PENDING' to allow for later confirmation or sync.
            insert_appointment = text("""
                INSERT INTO appointments (
                    appointment_id,
                    provider_id,
                    patient_id,
                    slot_time,
                    status,
                    retry_count
                )
                VALUES (
                    :appointment_id,
                    :provider_id,
                    :patient_id,
                    :slot_time,
                    'PENDING',
                    0
                )
                RETURNING id, appointment_id
            """)

            appt_result = session.execute(
                insert_appointment,
                {
                    "appointment_id": business_id,
                    "provider_id": slot_row.provider_id,
                    "patient_id": data["patient_id"],
                    "slot_time": slot_row.slot_time,
                },
            )
            new_record = appt_result.fetchone()

            # Critical: Commit both the UPDATE and the INSERT as a single transaction.
            # Either both succeed or both fail — no partial state.
            session.commit()

            return {
                "internal_id": str(new_record.id),
                "business_id": new_record.appointment_id,
            }

        except Exception:
            # Rollback ensures the slot is NOT marked unavailable
            # if appointment creation fails for any reason.
            session.rollback()
            raise
        finally:
            # Close connection back to the pool to avoid leaks.
            session.close()

    @staticmethod
    def get_by_provider(provider_id):
        """
        Fetch all appointments for a specific doctor.
        Converts datetime objects to ISO strings for JSON serialization.
        """
        session = SessionLocal()
        try:
            # Optimized Query: Filters by provider and sorts by the upcoming time.
            query = text("""
                SELECT
                    appointment_id,
                    patient_id,
                    slot_time,
                    status,
                    retry_count
                FROM appointments
                WHERE provider_id = :provider_id
                ORDER BY slot_time ASC
            """)
            result = session.execute(query, {"provider_id": provider_id})

            # List comprehension keeps mapping clean and readable.
            # slot_time is converted to ISO format so frontend can parse it easily.
            return [
                {
                    "appointment_id": row.appointment_id,
                    "patient_id": row.patient_id,
                    "slot_time": row.slot_time.isoformat(),
                    "status": row.status,
                    "retry_count": row.retry_count,
                }
                for row in result
            ]
        finally:
            # Read-only operation, but session still must be closed.
            session.close()

    @staticmethod
    def get_all():
        """
        Fetch every appointment across the system (Global/Admin view).
        Sorted by the most recently created.
        """
        session = SessionLocal()
        try:
            query = text("""
                SELECT
                    appointment_id,
                    provider_id,
                    patient_id,
                    slot_time,
                    status
                FROM appointments
                ORDER BY created_at DESC
            """)
            result = session.execute(query)

            # Data Mapping: Ensure slot_time is serializable.
            # This keeps API responses consistent across endpoints.
            return [
                {
                    "appointment_id": row.appointment_id,
                    "provider_id": row.provider_id,
                    "patient_id": row.patient_id,
                    "slot_time": row.slot_time.isoformat(),
                    "status": row.status,
                }
                for row in result
            ]
        finally:
            session.close()

    @staticmethod
    def cancel_appointment(appointment_id, cancelled_by="PROVIDER"):
        """
        Transactional logic for cancellation (PATCH):
        1. Set appointment status to 'CANCELLED'.
        2. Re-open the specific slot in 'provider_schedule'.
        """
        session = SessionLocal()
        try:
            # Step 1: Update appointment status
            # We explicitly block re-cancelling an already cancelled appointment.
            # RETURNING gives us the exact slot details needed to reopen availability.
            query_appt = text("""
                UPDATE appointments
                SET status = 'CANCELLED',
                    cancelled_by = :cancelled_by,
                    updated_at = NOW()
                WHERE appointment_id = :appointment_id
                  AND status != 'CANCELLED'
                RETURNING provider_id, slot_time
            """)
            result = session.execute(
                query_appt,
                {
                    "appointment_id": appointment_id,
                    "cancelled_by": cancelled_by,
                },
            )
            row = result.fetchone()

            # If row is None, the appointment_id was invalid
            # or the appointment was already cancelled.
            if not row:
                return False

            # Step 2: Release the Slot
            # Makes the slot visible in the available-slots API again.
            # Slot identity is time-based, not ID-based.
            query_slot = text("""
                UPDATE provider_schedule
                SET is_available = TRUE
                WHERE provider_id = :provider_id
                  AND slot_time = :slot_time
            """)
            session.execute(
                query_slot,
                {
                    "provider_id": row.provider_id,
                    "slot_time": row.slot_time,
                },
            )

            # Commit both status change and slot release together.
            session.commit()
            return True

        except Exception:
            # Any failure here must revert both appointment and slot state.
            session.rollback()
            raise
        finally:
            session.close()
            
    @staticmethod
    def get_provider_history(provider_id, start_date, end_date):
        """
        Fetches past appointments and basic analytics for a provider.
        """
        session = SessionLocal()
        try:
            # Query for the appointment list within the date range
            query = text("""
                SELECT appointment_id, patient_id, slot_time, status, cancelled_by
                FROM appointments 
                WHERE provider_id = :provider_id 
                AND slot_time BETWEEN :start_date AND :end_date
                ORDER BY slot_time DESC
            """)
            
            result = session.execute(query, {
                "provider_id": provider_id,
                "start_date": start_date,
                "end_date": end_date
            })
            
            appointments = []
            stats = {"total": 0, "completed": 0, "cancelled": 0}
            
            for row in result:
                appt = {
                    "appointment_id": row.appointment_id,
                    "patient_id": row.patient_id,
                    "slot_time": row.slot_time.isoformat(),
                    "status": row.status,
                    "cancelled_by": row.cancelled_by
                }
                appointments.append(appt)
                
                # Simple Analytics Logic
                stats["total"] += 1
                if row.status == 'COMPLETED':
                    stats["completed"] += 1
                elif row.status == 'CANCELLED':
                    stats["cancelled"] += 1

            return {"appointments": appointments, "stats": stats}
        finally:
            session.close()