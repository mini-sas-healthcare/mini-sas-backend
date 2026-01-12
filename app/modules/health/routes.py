from flask_restx import Namespace, Resource
from app.common.responses import success

ns = Namespace("health", description="Health check")

@ns.route("")
class Health(Resource):
    def get(self):
        return success({"status": "UP"})
