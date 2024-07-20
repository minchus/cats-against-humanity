import eventlet
from app import app, socket_io_app
from dotenv import load_dotenv
import os

load_dotenv()

os.environ['FLASK_ENV'] = 'development'
flask_port = os.environ.get('FLASK_PORT', 5000)
socket_io_app.run(app, host='0.0.0.0', port=flask_port, debug=True)
