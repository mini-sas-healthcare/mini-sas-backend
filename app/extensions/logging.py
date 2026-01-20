import logging
import sys

def configure_logging(app):
    # Define the log format
    log_format = "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    
    # Configure the root logger
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout) # Outputs to terminal/GCP logs
        ]
    )

    # Attach the logger to the Flask app
    app.logger.info("Logging has been initialized.")