from flask import Flask, current_app, send_file
from flask_socketio import SocketIO
import logging
import os


app = Flask(__name__, static_folder='../dist/static')
socket_io_app = SocketIO(app, cors_allowed_origins='*')

# from .api import api_bp
# app.register_blueprint(api_bp)

from app.cah import cah_bp
app.register_blueprint(cah_bp)

from .config import Config
logging.basicConfig(format="[%(pathname)s:%(lineno)s - %(funcName)s() ] %(message)s")
app.logger.info('>>> {}'.format(Config.FLASK_ENV))


@app.route('/')
def index_client():
    dist_dir = current_app.config['DIST_DIR']
    entry = os.path.join(dist_dir, 'index.html')
    return send_file(entry)


