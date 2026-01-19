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

# Swagger model for documentation
bulk_slot_model = schedule_ns.model('BulkSlotModel', {
    'start_time': fields.DateTime(required=True, example='2026-01-20T10:00:00'),
    'end_time': fields.DateTime(required=True, example='2026-01-20T14:00:00'),
    'interval_minutes': fields.Integer(required=True, example=30)
})

# 2. Endpoint: GET available slots
# This matches: GET /schedules/<provider_id>/available-slots
@schedule_ns.route("/<string:provider_id>/available-slots")
class AvailableSlots(Resource):
    def get(self, provider_id):
        """Fetch first 3 available slots for a specific provider"""
        # This calls your ScheduleService to query the DB
        return ScheduleService.get_provider_availability(provider_id)

@schedule_ns.route("/<string:provider_id>/bulk-slots")
class BulkSlotCreation(Resource):
    @schedule_ns.expect(bulk_slot_model)
    def post(self, provider_id):
        """Create multiple availability slots at once"""
        data = request.json
        return ScheduleService.generate_slots(provider_id, data)
