from app.modules.appointments.repository import AppointmentRepository
from app.common.responses import success

class AppointmentService:

# doctor side functionality
    @staticmethod
    def book(data):
        # In a real scenario, you'd call a PatientRepository here 
        # to check if 'is_verified' is True.
        
        result = AppointmentRepository.create_booking(data)
        
        if not result:
            return {
                "success": False,
                "data": None,
                "error": "Slot unavailable or invalid patient/slot data"
            }, 409 # 409 Conflict is better for 'already booked'
            
        return {
            "success": True,
            "data": result,
            "error": None
        }, 201
