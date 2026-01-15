from flask import request
from flask_restx import Namespace, Resource, fields
from app.modules.schedules.service import ScheduleService
# Import the actual service responsible for booking logic
from app.modules.appointments.service import AppointmentService 

schedule_ns = Namespace("schedules", description="Schedules and Availability")

# 1. Define models for Swagger UI JSON input
booking_input_model = schedule_ns.model('BookingInput', {
    'patient_id': fields.String(required=True, example='PAT-001', description='The business patient_id'),
    'slot_id': fields.String(required=True, example='uuid-goes-here', description='The UUID of the slot')
})

# 2. Endpoint: GET available slots
# This matches: GET /schedules/<provider_id>/available-slots
@schedule_ns.route("/<string:provider_id>/available-slots")
class AvailableSlots(Resource):
    def get(self, provider_id):
        """Fetch first 3 available slots for a specific provider"""
        # This calls your ScheduleService to query the DB
        return ScheduleService.get_provider_availability(provider_id)

# 3. Endpoint: POST booking
# This matches: POST /schedules/book
@schedule_ns.route("/book")
class BookProvider(Resource):
    @schedule_ns.expect(booking_input_model)
    def post(self):
        """Book an appointment using JSON data"""
        data = request.json
        
        # Validation for required fields
        if not data or 'patient_id' not in data or 'slot_id' not in data:
            return {
                "success": False,
                "data": None,
                "error": "Missing patient_id or slot_id in request body"
            }, 400

        # We call AppointmentService because booking is an "Appointment" domain task
        return AppointmentService.book(data)