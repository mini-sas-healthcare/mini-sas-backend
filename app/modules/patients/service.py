from app.modules.patients.repository import PatientRepository
from app.common.responses import success

class PatientService:

    @staticmethod
    def get_patient_by_id(patient_id):
        patient = PatientRepository.get_patient_by_id(patient_id)

        if not patient:
            return success({"message": "Patient not found"})

        return success(patient)
