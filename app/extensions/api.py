from flask_restx import Api
from app.modules.health.routes import health_ns
from app.modules.schedules.routes import schedule_ns
from app.modules.appointments.routes import appointment_ns
from app.modules.appointmentfdesk.routes import appointment_ns as frontdesk_appointment_ns

# If you want it at /swagger, you can set doc='/swagger'
api = Api(
    title="Mini-SAS API", 
    version="1.0", 
    description="Smart Appointment Scheduler",
    doc="/"  # This makes Swagger load at http://localhost:8080/
)

api.add_namespace(health_ns, path="/health")
api.add_namespace(schedule_ns, path="/schedules")
api.add_namespace(appointment_ns, path="/appointments")
api.add_namespace(frontdesk_appointment_ns, path="/appointments/frontdesk")