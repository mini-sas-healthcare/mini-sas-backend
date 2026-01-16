from flask_restx import Namespace, Resource, fields
from app.modules.appointmentfdesk.service import FrontDeskAppointmentService

appointment_ns = Namespace("appointments", description="Appointment APIs")

confirm_model = appointment_ns.model("ConfirmAppointment", {
    "appointment_id": fields.String(required=True)
})


@appointment_ns.route("/confirm")
class ConfirmAppointment(Resource):
    @appointment_ns.expect(confirm_model)
    def post(self):
        """
        Front Desk confirms an appointment
        """
        payload = appointment_ns.payload
        return FrontDeskAppointmentService.confirm_appointment(payload)
