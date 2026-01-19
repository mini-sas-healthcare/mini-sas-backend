from flask import request
from flask_restx import Namespace, Resource, fields
from app.extensions.db import SessionLocal
from sqlalchemy import text

patient_ns = Namespace("patients", description="Patient Management")

# Model for Swagger JSON input
patient_model = patient_ns.model('PatientModel', {
    'patient_id': fields.String(required=True, example='PAT-001'),
    'full_name': fields.String(required=True, example='Bhagirath Manda'),
    'phone_number': fields.String(example='1234567890'),
    'email': fields.String(example='test@example.com')
})

@patient_ns.route("")
class PatientList(Resource):
    @patient_ns.expect(patient_model)
    def post(self):
        """Add a new patient via JSON"""
        data = request.json
        session = SessionLocal()
        try:
            query = text("""
                INSERT INTO patients (patient_id, full_name, phone_number, email)
                VALUES (:patient_id, :full_name, :phone_number, :email)
                RETURNING id
            """)
            session.execute(query, data)
            session.commit()
            return {"success": True, "message": "Patient created"}, 201
        finally:
            session.close()


from flask_restx import Namespace, Resource
from app.modules.patients.service import PatientService


@patient_ns.route("/<string:patient_id>")
class GetPatient(Resource):
    def get(self, patient_id):
        """
        Get patient details by patient_id
        """
        return PatientService.get_patient_by_id(patient_id)
