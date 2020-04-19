import eventlet
from app import app, socketio

socketio.run(app, host='0.0.0.0', port=5000, debug=True)
# To Run:
# python run.py
# or
# python -m flask run
