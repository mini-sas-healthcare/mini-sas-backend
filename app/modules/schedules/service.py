from datetime import datetime
from app.modules.schedules.repository import ScheduleRepository

class ScheduleService:
    @staticmethod
    def get_provider_availability(provider_id):
        """
        Fetches available slots for a provider.
        This is the method the error log says is missing.
        """
        # Call the repository to get data from the database
        slots = ScheduleRepository.get_available_slots(provider_id)
        return {
            "success": True,
            "data": slots,
            "error": None
        }, 200

    @staticmethod
    def generate_slots(provider_id, data):
        """
        Logic to create multiple availability slots
        """
        try:
            # Parse the ISO strings from the Swagger request
            start_dt = datetime.fromisoformat(data['start_time'])
            end_dt = datetime.fromisoformat(data['end_time'])
            interval = int(data.get('interval_minutes', 30))
            
            count = ScheduleRepository.bulk_insert_slots(provider_id, start_dt, end_dt, interval)
            
            return {
                "success": True,
                "message": f"Successfully generated {count} slots",
                "data": {"slots_created": count}
            }, 201
        except Exception as e:
            return {"success": False, "error": str(e)}, 400