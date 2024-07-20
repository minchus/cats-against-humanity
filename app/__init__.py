from flask import Flask, current_app, send_file, send_from_directory
from flask_socketio import SocketIO
import logging
import os


app = Flask(__name__, static_folder='../dist/static')
socket_io_app = SocketIO(app, cors_allowed_origins='*')

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


@app.route('/favicon.ico')
def favicon():
    dist_dir = current_app.config['DIST_DIR']
    favicon = os.path.join(dist_dir, 'favicon.ico')
    return send_file(favicon)

