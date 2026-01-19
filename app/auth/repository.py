import bcrypt
from sqlalchemy import text
from app.extensions.db import SessionLocal

class AuthRepository:
    """
    Handles all database interactions for Authentication and User management.
    """

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Encrypts a plain-text password into a secure hash.
        """
        # Generate a salt and hash the password
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Compares a plain-text password with a stored hash to see if they match.
        """
        try:
            return bcrypt.checkpw(
                plain_password.encode('utf-8'), 
                hashed_password.encode('utf-8')
            )
        except Exception:
            return False

    @staticmethod
    def get_user_by_email(email: str):
        """
        Finds a user in the database by their email address.
        Used during the login process to verify credentials and check roles.
        """
        session = SessionLocal()
        try:
            # We fetch the role and password_hash to support JWT and RBAC later
            query = text("""
                SELECT id, email, role, password_hash, is_active 
                FROM users 
                WHERE email = :email
            """)
            result = session.execute(query, {"email": email}).fetchone()
            
            # Return as a dictionary or None if not found
            return dict(result._mapping) if result else None
        finally:
            session.close()