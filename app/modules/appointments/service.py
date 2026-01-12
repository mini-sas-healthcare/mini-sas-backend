from app.modules.appointments.repository import AppointmentRepository
from app.common.responses import success

class AppointmentService:

    @staticmethod
    def book():
        AppointmentRepository.create()
        return success({"status": "RESERVED"})
