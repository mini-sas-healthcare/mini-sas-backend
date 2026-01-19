from app.modules.appointments.repository import AppointmentRepository
from app.common.responses import success

class AppointmentService:

# doctor side functionality
    @staticmethod
    def book(data):
        """Logic to create a new booking"""
        # Note: Future integration point for Patient verification check
        result = AppointmentRepository.create_booking(data)
        
        if not result:
            return {
                "success": False,
                "data": None,
                "error": "Slot unavailable or invalid patient/slot data"
            }, 409 
            
        return {
            "success": True,
            "data": result,
            "error": None
        }, 201
        
    @staticmethod
    def get_provider_schedule(provider_id):
        """Logic for provider-specific viewing"""
        appointments = AppointmentRepository.get_by_provider(provider_id)
        return {
            "success": True,
            "data": appointments,
            "error": None
        }, 200

    @staticmethod
    def get_all_appointments():
        """Logic for system-wide viewing"""
        appointments = AppointmentRepository.get_all()
        return {
            "success": True,
            "data": appointments,
            "error": None
        }, 200
    
    @staticmethod
    def cancel(appointment_id, data):
        """Logic to cancel an existing appointment"""
        # Extract actor from JSON body, defaulting to PROVIDER
        cancelled_by = data.get('cancelled_by', 'PROVIDER')
        success = AppointmentRepository.cancel_appointment(appointment_id, cancelled_by)

        if not success:
            return {
                "success": False, 
                "data": None,
                "error": "Appointment not found or already cancelled"
            }, 404
        
        return {
            "success": True, 
            "data": {"appointment_id": appointment_id},
            "error": None
        }, 200
