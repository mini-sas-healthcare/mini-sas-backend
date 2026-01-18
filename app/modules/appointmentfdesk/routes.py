from flask_restx import Namespace, Resource, fields
from app.modules.appointmentfdesk.service import FrontDeskAppointmentService

appointment_ns = Namespace("appointments", description="Appointment APIs")

billing_model = appointment_ns.model("BillingData", {
    "patient_id": fields.String(required=True),
    "provider_id": fields.String(required=True),
    "cpt_code": fields.String(required=True),
    "payer_code": fields.String(required=True),
    "amount": fields.Float(required=True),
})

confirm_model = appointment_ns.model("ConfirmAppointment", {
    "appointment_id": fields.String(required=True),
    "billing": fields.Nested(billing_model, required=False)
})


@appointment_ns.route("/confirm")
class ConfirmAppointment(Resource):
    @appointment_ns.expect(confirm_model)
    def post(self):
        """
        Front Desk confirms an appointment and optionally creates billing (PENDING)
        """
        payload = appointment_ns.payload
        return FrontDeskAppointmentService.confirm_appointment(payload)
