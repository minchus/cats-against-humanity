from flask import Blueprint, request
from flask_socketio import SocketIO, join_room, leave_room, close_room, send, emit

from app import socketio
from app.cah import game

cah_bp = Blueprint('cah', __name__,
                   url_prefix='',
                   static_url_path='',
                   static_folder='./dist/static/',
                   template_folder='./dist/',
                   )

ROOMS = {}

# def prune():
#     """Prune rooms stale for more than 6 hours"""
#     def delete_room(gid):
#         close_room(gid)
#         del ROOMS[gid]
#
#     def is_stale(room):
#         """Stale rooms are older than 6 hours, or have gone 20 minutes less than 5 minutes of total playtime"""
#         return (((datetime.now() - room.date_modified).total_seconds() >= (60*60*24)) or
#                 ((datetime.now() - room.date_modified).total_seconds() >= (60*20) and
#                  room.playtime() <= 5))
#
#     if ROOMS:
#         rooms = ROOMS.copy()
#         for key in rooms.keys():
#             if is_stale(ROOMS[key]):
#                 delete_room(key)
#         del rooms
#         gc.collect()


# @app.route('/stats')
# def stats():
#     """display room stats"""
#     resp = {
#         "total": len(ROOMS.keys()),
#         "bytes_used": getsizeof(ROOMS)
#     }
#     if 'rooms' in request.args:
#         if ROOMS:
#             resp["rooms"] = sorted([ v.to_json() for v in ROOMS.values() ], key=lambda k: k.get('date_modified'), reverse=True)
#         else:
#             resp["rooms"] = None
#     return jsonify(resp)


@socketio.on('create')
def on_create(data):
    """Create a new game"""
    try:
        username = data['username']
        gm = game.GameState()
        room = gm.game_id
        ROOMS[room] = gm
        join_room(room)
        # rooms[room].add_player(username)
        emit('join_room', {'room': room})
        # prune()
    except Exception as e:
        emit('join_room', {'error': f"Unable to create game"})


@socketio.on('join')
def on_join(data):
    """Join a game lobby"""
    # username = data['username']
    room = data['room']
    if room in ROOMS:
        # add player and rebroadcast game object
        # rooms[room].add_player(username)
        join_room(room)
        send(ROOMS[room].to_json(), room=room)
    else:
        emit('error', {'error': 'Unable to join room. Room does not exist.'})


@socketio.on('leave')
def on_leave(data):
    """Leave the game lobby"""
    # username = data['username']
    room = data['room']
    # add player and rebroadcast game object
    # rooms[room].remove_player(username)
    leave_room(room)
    send(ROOMS[room].to_json(), room=room)


# @socketio.on('flip_card')
# def on_flip_card(data):
#     """flip card and rebroadcast game object"""
#     ROOMS[data['room']].flip_card(data['card'])
#     send(ROOMS[data['room']].to_json(), room=data['room'])


# @socketio.on('regenerate')
# def on_regenerate(data):
#     """regenerate the words list"""
#     room = data['room']
#     ROOMS[room].generate_board(data.get('newGame', False))
#     send(ROOMS[room].to_json(), room=room)


# @socketio.on('list_dictionaries')
# def list_dictionaries():
#     """send a list of dictionary names"""
#     # send dict list to client
#     emit('list_dictionaries', {'dictionaries': list(game.DICTIONARIES.keys())})


