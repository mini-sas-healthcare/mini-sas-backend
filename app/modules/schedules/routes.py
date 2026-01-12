from flask_restx import Namespace, Resource

ns = Namespace("providers", description="Provider scheduling")

@ns.route("/<string:provider_id>/slots")
class ProviderSlots(Resource):
    def get(self, provider_id):
        return {"success": True, "data": [], "error": None}
