from app.modules.schedules.repository import ScheduleRepository

class ScheduleService: # Fixed spelling from 'Shedule' to 'Schedule'
    @staticmethod
    def get_provider_availability(provider_id):
        #todo :- have to add many logics like checking provider exist or not, i will do it later if time permits
        return ScheduleRepository.get_available_slots(provider_id)