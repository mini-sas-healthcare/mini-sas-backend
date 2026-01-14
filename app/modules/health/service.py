from app.modules.health.repository import HealthRepository

class HealthService:
    @staticmethod
    def check_health():
        db_status = HealthRepository.ping_db()
        return {
            "status": "UP",
            "database": "UP" if db_status else "DOWN"
        }