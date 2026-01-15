from flask_restx import Namespace, Resource
from app.modules.schedules.service import ScheduleService

schedule_ns = Namespace("schedules", description="Provider Availability APIs")

@schedule_ns.route("/<string:provider_id>/available-slots")
class AvailableSlots(Resource):
    def get(self, provider_id):
        """Fetch first 3 available slots for a specific provider"""
        slots = ScheduleService.get_provider_availability(provider_id)
        
        return {
            "success": True,
            "data": slots,
            "error": None
        }, 200