from flask_restx import Namespace, Resource

# This variable name MUST match the import in api.py
schedule_ns = Namespace('schedules', description='Provider schedule operations')

@schedule_ns.route('/<string:provider_id>/available-slots')
class AvailableSlots(Resource):
    def get(self, provider_id):
        """Fetch first 3 available slots for a provider"""
        # Skeleton response for now
        return {
            "success": True,
            "data": [],
            "error": None
        }, 200