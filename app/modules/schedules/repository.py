from sqlalchemy import text
from app.extensions.db import SessionLocal

class ScheduleRepository:  # Ensure this is spelled correctly
    @staticmethod
    def get_available_slots(provider_id, limit=3):
        session = SessionLocal()
        try:
            query = text("""
                SELECT id, slot_time 
                FROM provider_schedule 
                WHERE provider_id = :provider_id 
                AND is_available = TRUE 
                ORDER BY slot_time ASC 
                LIMIT :limit
            """)
            result = session.execute(query, {"provider_id": provider_id, "limit": limit})
            
            # Use ._mapping to handle SQLAlchemy Core Row objects in 2.0+
            return [{"slot_id": str(row.id), "slot_time": row.slot_time.isoformat()} for row in result]
        finally:
            session.close()