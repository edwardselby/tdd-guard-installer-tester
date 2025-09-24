#!/usr/bin/env python3
"""Development server runner."""
import os
from app import create_app

if __name__ == '__main__':
    config_name = os.environ.get('FLASK_ENV', 'development')
    app = create_app(config_name)

    host = os.environ.get('FLASK_RUN_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_RUN_PORT', 5000))
    debug = config_name == 'development'

    app.run(host=host, port=port, debug=debug)