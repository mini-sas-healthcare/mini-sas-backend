from flask_restx import Namespace, Resource, fields
from app.modules.billing.service import FrontDeskBillingService
# Import the roles_required decorator
from app.auth.decorators import roles_required

# Added security='Bearer' to enable the lock icon in Swagger
billing_ns = Namespace(
    "billing",
    description="Appointment Billing APIs",
    security='Bearer'
)

complete_model = billing_ns.model("CompleteBilling", {
    "appointment_id": fields.String(required=True)
})

@billing_ns.route("/complete")
class CompleteBilling(Resource):
    @billing_ns.doc(security='Bearer') # Document security for this endpoint
    @roles_required('FRONTDESK')      # Restrict access to FRONTDESK only
    @billing_ns.expect(complete_model)
    def post(self):
        """
        Mark appointment billing as COMPLETED
        """
        payload = billing_ns.payload
        return FrontDeskBillingService.complete_billing(payload)