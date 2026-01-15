from flask_restx import Namespace, Resource
from app.modules.health.service import HealthService

# Namespace for Swagger documentation
health_ns = Namespace('health', description='Health Check Operations')

@health_ns.route('')
class HealthResource(Resource):
    def get(self):
        """Service status and DB connectivity check"""
        health_data = HealthService.check_health()
        
        # Frozen Response Envelope
        return {
            "success": True,
            "data": health_data,
            "error": None
        }, 200