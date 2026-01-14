from flask_restx import Namespace, Resource
from app.modules.appointments.service import AppointmentService

# Renamed 'ns' to 'appointment_ns' to match app/extensions/api.py
appointment_ns = Namespace("appointments", description="Appointment APIs")

@appointment_ns.route("/book")
class BookAppointment(Resource):
    def post(self):
        """Book a new appointment"""
        return AppointmentService.book()