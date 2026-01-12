from functools import wraps
from flask import request

def require_role(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            role = request.headers.get("X-ROLE")
            if role not in roles:
                return {"success": False, "data": None, "error": "Access denied"}, 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
