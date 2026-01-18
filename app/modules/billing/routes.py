from flask_restx import Namespace, Resource, fields
from app.modules.billing.service import FrontDeskBillingService

billing_ns = Namespace("billing", description="Appointment Billing APIs")

complete_model = billing_ns.model("CompleteBilling", {
    "appointment_id": fields.String(required=True)
})


@billing_ns.route("/complete")
class CompleteBilling(Resource):
    @billing_ns.expect(complete_model)
    def post(self):
        """
        Mark appointment billing as COMPLETED
        """
        payload = billing_ns.payload
        return FrontDeskBillingService.complete_billing(payload)
