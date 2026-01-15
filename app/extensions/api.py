from flask_restx import Api

# Initialize the Api object
api = Api(
    title="Mini-SAS API",
    version="1.0",
    description="Smart Appointment Scheduler Backend",
    doc="/swagger"
)

# Import Namespaces from Module Routes
# Note: Ensure the variable names in your routes.py match these imports
from app.modules.health.routes import health_ns
from app.modules.schedules.routes import schedule_ns
from app.modules.appointments.routes import appointment_ns

# Register Namespaces
# /health -> System health and DB ping
api.add_namespace(health_ns, path="/health")

# /providers -> Provider availability and slot fetching
api.add_namespace(schedule_ns, path="/providers")

# /appointments -> Booking and lifecycle management
api.add_namespace(appointment_ns, path="/appointments")