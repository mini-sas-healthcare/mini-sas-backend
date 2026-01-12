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
