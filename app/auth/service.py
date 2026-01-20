import jwt
import datetime
import os
import logging
from app.auth.repository import AuthRepository

# Initialize logger for this specific module
logger = logging.getLogger(__name__)

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

        logger.info(f"Login attempt initiated for email: {email}") # Log the start of the process

        # 1. Fetch user from DB
        try:
            user = AuthRepository.get_user_by_email(email)
        except Exception as e:
            logger.error(f"Database error during login for {email}: {str(e)}") # Log critical DB failures
            return {"success": False, "error": "Internal server error"}, 500

        # 2. Verify existence and password hash
        if not user or not AuthRepository.verify_password(password, user['password_hash']):
            logger.warning(f"Unauthorized access attempt: Invalid credentials for email {email}") # Log security warnings
            return {
                "success": False, 
                "error": "Invalid email or password"
            }, 401

        # 3. Generate JWT Payload
        try:
            payload = {
                "user_id": str(user['id']),
                "role": user['role'],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }

            # 4. Sign the token
            token = jwt.encode(
                payload, 
                os.getenv("JWT_SECRET_KEY"), 
                algorithm=os.getenv("JWT_ALGORITHM", "HS256")
            )

            logger.info(f"Successfully authenticated user: {email} with role: {user['role']}") # Log successful login
            
            return {
                "success": True,
                "token": token,
                "role": user['role']
            }, 200

        except Exception as e:
            logger.error(f"JWT generation failed for {email}: {str(e)}") # Log token creation errors
            return {"success": False, "error": "Could not generate authentication token"}, 500