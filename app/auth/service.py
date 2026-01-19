import jwt
import datetime
import os
from app.auth.repository import AuthRepository

class AuthService:
    """
    Coordinates user authentication and token generation.
    """

    @staticmethod
    def login(data):
        """
        Verifies credentials and returns a JWT if successful.
        """
        email = data.get('email')
        password = data.get('password')

        # 1. Fetch user from DB
        user = AuthRepository.get_user_by_email(email)

        # 2. Verify existence and password hash
        if not user or not AuthRepository.verify_password(password, user['password_hash']):
            return {
                "success": False, 
                "error": "Invalid email or password"
            }, 401

        # 3. Generate JWT Payload
        # We include the role to support Role-Based Access Control later.
        payload = {
            "user_id": str(user['id']),
            "role": user['role'],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24) # Token lasts 24 hours
        }

        # 4. Sign the token
        token = jwt.encode(
            payload, 
            os.getenv("JWT_SECRET_KEY"), 
            algorithm=os.getenv("JWT_ALGORITHM", "HS256")
        )

        return {
            "success": True,
            "token": token,
            "role": user['role']
        }, 200