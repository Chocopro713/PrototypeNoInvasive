from flask import Flask
from app.config import Config
from app.database import create_db_connection
from app.routes import blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Registrar automáticamente todos los Blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

    return app
