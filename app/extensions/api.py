from flask_restx import Api
from app.modules.health.routes import health_ns
from app.modules.schedules.routes import schedule_ns
from app.modules.appointments.routes import appointment_ns
from app.modules.billing.routes import billing_ns
from app.modules.appointmentfdesk.routes import appointment_ns as frontdesk_appointment_ns
from app.modules.patients.routes import patient_ns
from app.auth.routes import auth_ns
from flask_restx import Api

# Define the authorization scheme
authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Input format: Bearer <your_jwt_token>"
    }
}

api = Api(
    title="Mini-SAS Healthcare API",
    version="1.0",
    description="Backend for Appointment Management",
    authorizations=authorizations, # Enable security in Swagger
    security='Bearer'              # Apply it globally (optional)
)

api.add_namespace(auth_ns, path="/auth")
api.add_namespace(health_ns, path="/health")
api.add_namespace(schedule_ns, path="/schedules")
api.add_namespace(appointment_ns, path="/appointments")
api.add_namespace(frontdesk_appointment_ns, path="/appointments/frontdesk")
api.add_namespace(billing_ns, path="/billing")
api.add_namespace(patient_ns, path="/patients")