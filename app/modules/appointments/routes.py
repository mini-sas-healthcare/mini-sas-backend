from flask import request
from flask_restx import Namespace, Resource
from app.modules.appointments.service import AppointmentService

appointment_ns = Namespace("appointments", description="Appointment Booking APIs")

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