from flask_restx import Api

api = Api(
    title="Mini-SAS API",
    version="1.0",
    description="Smart Appointment Scheduler Backend",
    doc="/swagger"
)

from app.modules.health.routes import ns as health_ns
from app.modules.appointments.routes import ns as appointment_ns
from app.modules.schedules.routes import ns as schedule_ns

api.add_namespace(health_ns, path="/health")
api.add_namespace(appointment_ns, path="/appointments")
api.add_namespace(schedule_ns, path="/providers")
