from flask_pymongo import PyMongo
from pymongo.errors import ConnectionFailure
import mongomock

mongo = PyMongo()


def init_db(app):
    """Initialize database connection."""
    if app.config.get('TESTING'):
        # Use mongomock for testing
        app.config['MONGO_URI'] = 'mongodb://localhost:27017/test'
        mongo.init_app(app)
        # Replace the PyMongo client with mongomock for testing
        mongo.cx = mongomock.MongoClient()
        mongo.db = mongo.cx.get_database('test_task_tracker')
    else:
        mongo.init_app(app)
        # Test connection for non-testing environments
        try:
            mongo.cx.server_info()
            app.logger.info("Successfully connected to MongoDB")
        except ConnectionFailure as e:
            app.logger.error(f"Could not connect to MongoDB: {e}")
            raise