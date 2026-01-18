from app.modules.billing.repository import FrontDeskBillingRepository
from app.common.responses import success

class FrontDeskBillingService:

    @staticmethod
    def complete_billing(data):
        appointment_id = data["appointment_id"]

        result = FrontDeskBillingRepository.complete_billing(
            appointment_id=appointment_id
        )

        if result == "NOT_FOUND":
            return success({"message": "Billing record not found"})

        if result == "ALREADY_COMPLETED":
            return success({"message": "Billing already completed"})

        return success({"status": "COMPLETED"})
