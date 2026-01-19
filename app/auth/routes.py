from flask import request
from flask_restx import Namespace, Resource, fields
from app.auth.service import AuthService

auth_ns = Namespace("auth", description="Authentication Operations")

# Swagger model for documentation
login_model = auth_ns.model('LoginModel', {
    'email': fields.String(required=True, example='bhagirathmanda.csi@gmail.com'),
    'password': fields.String(required=True, example='Provider@123')
})

@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        """Verify credentials and receive a JWT"""
        data = request.json
        return AuthService.login(data)