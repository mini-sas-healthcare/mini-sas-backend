import jwt
import os
from functools import wraps
from flask import request

def token_required(f):
    """
    Decorator to verify the JWT token in the request header.
    Supports both 'Bearer <token>' and raw '<token>' formats.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Using .get() ensures we don't crash if the header is missing
        auth_header = request.headers.get('Authorization')

        if auth_header:
            # Check if the header contains the Bearer prefix
            if auth_header.startswith("Bearer "):
                # Split and take the second part (the actual token)
                token = auth_header.split(" ")[1]
            else:
                # If no prefix, assume the whole header is the token
                token = auth_header

        if not token:
            return {"success": False, "error": "Token is missing!"}, 401

        try:
            # Decode the token using environment variables
            data = jwt.decode(
                token, 
                os.getenv("JWT_SECRET_KEY"), 
                algorithms=[os.getenv("JWT_ALGORITHM", "HS256")]
            )
            # Inject user data into the request context for use in routes
            request.user = data 
        except jwt.ExpiredSignatureError:
            return {"success": False, "error": "Token has expired!"}, 401
        except Exception as e:
            return {"success": False, "error": f"Invalid token: {str(e)}"}, 401

        return f(*args, **kwargs)

    return decorated

def roles_required(*roles):
    """
    Decorator to restrict access based on user roles (e.g., PROVIDER, PATIENT).
    """
    def wrapper(f):
        @wraps(f)
        @token_required # Validates the token before checking roles
        def decorated(*args, **kwargs):
            # Verify if the user's role is in the authorized list
            if request.user.get('role') not in roles:
                return {
                    "success": False, 
                    "error": f"Access denied. Required roles: {roles}"
                }, 403
            return f(*args, **kwargs)
        return decorated
    return wrapper