import logging
import sys

# Rename this to match your main.py call
def init_logging(app):
    """
    Initializes the logging configuration for the Flask application.
    """
    log_format = "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout) # Crucial for GCP Cloud Logging
        ]
    )

    app.logger.info("Logging extension initialized successfully.")