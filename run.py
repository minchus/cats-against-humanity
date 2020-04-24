import eventlet
from app import app, socket_io_app
import os

os.environ['FLASK_ENV'] = 'development'
socket_io_app.run(app, host='0.0.0.0', port=5000, debug=True)
