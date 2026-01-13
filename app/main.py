from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from app.extensions.api import api
from app.extensions.db import init_db
from app.extensions.logging import init_logging
from app.config.development import DevelopmentConfig

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    init_logging(app)
    init_db(app)
    api.init_app(app)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
