from flask import Blueprint, request
import flask_socketio as sio

from app import socket_io_app, app
from app.cah.game import RoomManager, Game

cah_bp = Blueprint('cah', __name__,
                   url_prefix='',
                   static_url_path='',
                   static_folder='./dist/static/',
                   template_folder='./dist/',
                   )


# @app.route('/stats')
# def stats():
#     """display room stats"""
#     resp = {
#         "total": len(ROOMS.keys()),
#         "bytes_used": getsizeof(ROOMS)
#     }
#     if 'rooms' in request.args:
#         if ROOMS:
#             resp["rooms"] = sorted([ v.to_json() for v in ROOMS.values() ],
#                                    key=lambda k: k.get('date_modified'), reverse=True)
#         else:
#             resp["rooms"] = None
#     return jsonify(resp)


@socket_io_app.on('create')
def on_create(data):
    app.logger.info(data)
    g = RoomManager.create_game(first_player_name=data['username'])
    app.logger.info(f"Created game with room code {g.room_code}")
    sio.join_room(g.room_code)
    sio.send(g.serialize(), room=g.room_code)
    RoomManager.prune()


@socket_io_app.on('join')
def on_join(data):
    app.logger.info(data)
    room_code = data['room']
    username = data['username']
    try:
        g = RoomManager.get_game(room_code=room_code)
        g.add_player(name=username)
        sio.join_room(g.room_code)
        sio.send(g.serialize(), room=g.room_code)
    except RoomManager.NoRoomError:
        sio.emit('error', {'error': 'Unable to join room. Room does not exist.'})
    except Game.PlayerExistsError:
        sio.emit('error', {'error': f'Unable to join room. A player with name {username} already exists.'})


@socket_io_app.on('leave')
def on_leave(data):
    app.logger.info(data)
    room_code = data['room']
    username = data['username']
    g = RoomManager.get_game(room_code=room_code)
    g.remove_player(name=username)
    sio.leave_room(room_code)
    sio.send(g.serialize(), room=g.room_code)
