from dotenv import load_dotenv
load_dotenv()

import logging
from flask import Flask, jsonify
from app.extensions.api import api
from app.extensions.db import init_db
from app.extensions.logging import init_logging
from app.config.development import DevelopmentConfig

# Initialize a logger for this file
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    # 1. Initialize Logging and DB
    init_logging(app)
    init_db(app)

    # 2. Add the Global Error Handler
    @app.errorhandler(Exception)
    def handle_global_exception(e):
        """
        Safety net that catches any crash in any module.
        """
        # This captures the line number and file where the crash happened
        logger.error(f"Unexpected Error: {str(e)}", exc_info=True)
        
        return jsonify({
            "success": False,
            "error": "Internal Server Error",
            "message": "An unexpected error occurred on the server."
        }), 500

    # 3. Initialize API
    api.init_app(app)

    return app

app = create_app()

if __name__ == "__main__":
    # Standard host/port for local and GCP compatibility
    app.run(host="0.0.0.0", port=8080, debug=True)