from flask import request
from flask_restx import Namespace, Resource
from app.modules.appointments.service import AppointmentService

appointment_ns = Namespace("appointments", description="Appointment Booking APIs")
appointment_ns = Namespace("appointments", description="Appointment Management APIs")

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
@appointment_ns.route("/book")
class BookAppointment(Resource):
    def post(self):
        """
        Book a new appointment. 
        Note: This endpoint ONLY accepts POST requests.
        """
        data = request.get_json()
        
        # Validation: Ensure we have the necessary strings
        if not data or 'patient_id' not in data or 'slot_id' not in data:
            return {
                "success": False, 
                "data": None, 
                "error": "Missing patient_id or slot_id"
            }, 400
            
        return AppointmentService.book(data)