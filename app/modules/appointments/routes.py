from flask_restx import Namespace, Resource
from app.modules.appointments.service import AppointmentService

ns = Namespace("appointments", description="Appointment APIs")

@ns.route("/book")
class BookAppointment(Resource):
    def post(self):
        return AppointmentService.book()
