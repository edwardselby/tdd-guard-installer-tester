from flask import Flask
from flask_cors import CORS

from app.config import config_by_name
from app.database import init_db


def create_app(config_name='development'):
    """Application factory pattern."""
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions
    CORS(app)
    init_db(app)

    # Register blueprints
    from app.blueprints.tasks import tasks_bp
    app.register_blueprint(tasks_bp, url_prefix='/api')

    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'service': 'task-tracker-api'}, 200

    return app