from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import app_config

db = SQLAlchemy()


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(app_config['development'])

    db.init_app(app)

    with app.app_context():
        from . import views  # Import routes
        db.create_all()  # Create sql tables for our data models

    return app
