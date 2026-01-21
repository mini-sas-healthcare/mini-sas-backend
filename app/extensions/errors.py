import logging
from flask import jsonify

logger = logging.getLogger(__name__)

def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        """
        Global safety net for any unhandled exceptions.
        """
        # Log the full error details for the developer
        logger.error(f"Unhandled Exception: {str(e)}", exc_info=True)

        # Return a generic, safe message to the user
        response = {
            "success": False,
            "error": "An unexpected error occurred. Please try again later.",
            "type": e.__class__.__name__
        }
        
        return jsonify(response), 500