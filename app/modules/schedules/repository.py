from sqlalchemy import text
from app.extensions.db import SessionLocal
from datetime import timedelta

class ScheduleRepository:
    @staticmethod
    def get_available_slots(provider_id):
        """Fetches the first 3 available slots"""
        session = SessionLocal()
        try:
            # We filter for is_available = TRUE
            query = text("""
                SELECT id, slot_time 
                FROM provider_schedule 
                WHERE provider_id = :provider_id AND is_available = TRUE
                ORDER BY slot_time ASC
                LIMIT 3
            """)
            result = session.execute(query, {"provider_id": provider_id})
            # Convert to ISO format to avoid JSON serializable errors
            return [{"slot_id": str(row.id), "slot_time": row.slot_time.isoformat()} for row in result]
        finally:
            session.close()

    @staticmethod
    def bulk_insert_slots(provider_id, start_time, end_time, interval_minutes):
        """Transactional logic for bulk slot creation"""
        session = SessionLocal()
        try:
            slots_to_insert = []
            current_time = start_time
            
            while current_time < end_time:
                slots_to_insert.append({
                    "provider_id": provider_id,
                    "slot_time": current_time,
                    "is_available": True
                })
                current_time += timedelta(minutes=interval_minutes)
            
            query = text("""
                INSERT INTO provider_schedule (provider_id, slot_time, is_available)
                VALUES (:provider_id, :slot_time, :is_available)
            """)
            
            session.execute(query, slots_to_insert)
            session.commit()
            return len(slots_to_insert)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()