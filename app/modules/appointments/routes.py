from flask import request
from flask_restx import Namespace, Resource, fields
from app.modules.appointments.service import AppointmentService

# Single definition for the namespace
appointment_ns = Namespace("appointments", description="Appointment Management APIs")

# --- Swagger Models ---
# Model for Booking
booking_model = appointment_ns.model('BookingModel', {
    'patient_id': fields.String(required=True, example='PAT-001'),
    'slot_id': fields.String(required=True, example='uuid-of-the-slot')
})

# Model for Cancellation (optional fields)
cancel_model = appointment_ns.model('CancelModel', {
    'cancelled_by': fields.String(required=False, example='PROVIDER', description='Who is cancelling')
})

# --- Routes ---

@appointment_ns.route("/book")
class BookAppointment(Resource):
    @appointment_ns.expect(booking_model)
    def post(self):
        """Book a new appointment"""
        data = request.get_json()
        
        if not data or 'patient_id' not in data or 'slot_id' not in data:
            return {
                "success": False, 
                "data": None, 
                "error": "Missing patient_id or slot_id"
            }, 400
            
        return AppointmentService.book(data)

@appointment_ns.route("/<string:appointment_id>/cancel")
class CancelAppointment(Resource):
    @appointment_ns.expect(cancel_model)
    def patch(self, appointment_id):
        """Cancel an appointment and release the slot"""
        data = request.json or {}
        return AppointmentService.cancel(appointment_id, data)

@appointment_ns.route("/provider/<string:provider_id>")
class ProviderAppointments(Resource):
    def get(self, provider_id):
        """Fetch appointments for a specific doctor"""
        appointments = AppointmentService.get_provider_schedule(provider_id)
        return {"success": True, "data": appointments}, 200

@appointment_ns.route("/all")
class AllAppointments(Resource):
    def get(self):
        """Fetch all appointments across the system"""
        appointments = AppointmentService.get_all_appointments()
        return {"success": True, "data": appointments}, 200


@appointment_ns.route("/provider/<string:provider_id>/history")
class AppointmentHistory(Resource):
    @appointment_ns.doc(params={
        'start_date': 'ISO format start date (e.g. 2026-01-01T00:00:00)',
        'end_date': 'ISO format end date'
    })
    def get(self, provider_id):
        """Fetch appointment history and analytics for a provider"""
        params = request.args # Extracts ?start_date=... from URL
        return AppointmentService.get_history(provider_id, params)