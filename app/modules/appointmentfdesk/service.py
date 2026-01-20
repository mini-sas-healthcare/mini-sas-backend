from app.modules.appointmentfdesk.repository import FrontDeskAppointmentRepository
from app.common.responses import success

class FrontDeskAppointmentService:

    @staticmethod
    def confirm_appointment(data):
        appointment_id = data["appointment_id"]
        billing_data = data.get("billing")

        result = FrontDeskAppointmentRepository.confirm_appointment(
            appointment_id=appointment_id,
            billing_data=billing_data
        )

        if result == "NOT_FOUND":
            return success({"message": "Appointment not found"})

        if result == "ALREADY_CONFIRMED":
            return success({"message": "Appointment already confirmed"})

        return success({
            "status": "CONFIRMED",
            "billing": "CREATED" if billing_data else "SKIPPED"
        })
    

    @staticmethod
    def get_pending_appointments():
        appointments = (
            FrontDeskAppointmentRepository.get_pending_appointments()
        )
        return success(appointments)


    @staticmethod
    def get_todays_appointments():
        appointments = (
            FrontDeskAppointmentRepository.get_todays_appointments()
        )
        return success(appointments)