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
#     '''display room stats'''
#     resp = {
#         'total': len(ROOMS.keys()),
#         'bytes_used': getsizeof(ROOMS)
#     }
#     if 'rooms' in request.args:
#         if ROOMS:
#             resp['rooms'] = sorted([ v.to_json() for v in ROOMS.values() ],
#                                    key=lambda k: k.get('date_modified'), reverse=True)
#         else:
#             resp['rooms'] = None
#     return jsonify(resp)


@socket_io_app.on('create')
def on_create(data):
    app.logger.debug(data)
    g = RoomManager.create_game(first_player_name=data['username'])
    app.logger.debug(f'Created game with room code {g.room_code}')
    sio.join_room(g.room_code)
    sio.send(g.serialize(), room=g.room_code)
    RoomManager.prune()


@socket_io_app.on('join')
def on_join(data):
    app.logger.debug(data)
    room_code = data['room']
    username = data['username']
    first_time = data['firstTime']
    try:
        g = RoomManager.get_game(room_code=room_code)
        if first_time:
            g.add_player(name=username)
        sio.join_room(g.room_code)
        app.logger.debug(f'User {username} joined {room_code}')
        sio.send(g.serialize(), room=g.room_code)
    except RoomManager.NoRoomError:
        app.logger.debug(f'User {username} tried to join {room_code} but room did not exist')
        sio.emit('error', {'error': 'Room does not exist.'})
    except Game.PlayerExistsError:
        app.logger.debug(f'User {username} tried to join {room_code} but user already exists')
        sio.emit('error', {'error': f'A player with name {username} already exists in room {room_code}.'})


@socket_io_app.on('leave')
def on_leave(data):
    app.logger.info(data)
    room_code = data['room']
    username = data['username']
    g = RoomManager.get_game(room_code=room_code)
    g.remove_player(name=username)
    sio.leave_room(room_code)
    sio.send(g.serialize(), room=g.room_code)


@socket_io_app.on('submit')
def on_submit(data):
    app.logger.info(data)
    room_code = data['room']
    username = data['username']
    submission = data['submission']
    submitted_cards = data['submittedCards']
    try:
        g = RoomManager.get_game(room_code=room_code)
        g.add_submission(player_name=username, submission=submission, submitted_cards=submitted_cards)
        sio.send(g.serialize(), room=g.room_code)
    except RoomManager.NoRoomError:
        app.logger.debug(f'User {username} tried to join {room_code} but room did not exist')
        sio.emit('error', {'error': f'Room {room_code} does not exist.'})
    except Game.PlayerNotExistsError:
        app.logger.debug(f'Submission received from non-existent user: {username}')
        sio.emit('error', {'error': f'Submission received from non-existent user: {username}'})
    except Game.PlayerAlreadySubmittedError:
        app.logger.debug(f'Submission already received from user: {username}')
        sio.emit('error', {'error': f'Submission already received from user: {username}'})


@socket_io_app.on('reveal')
def on_reveal(data):
    app.logger.info(data)
    room_code = data['room']
    username = data['username']
    try:
        g = RoomManager.get_game(room_code=room_code)
        g.reveal_submission(player_name=username)
        sio.send(g.serialize(), room=g.room_code)
    except Game.PlayerNotExistsError:
        app.logger.debug(f'Player does not exist: {username}')
        sio.emit('error', {'error': f'Player does not exist: {username}'})


@socket_io_app.on('pick')
def on_pick(data):
    app.logger.info(data)
    room_code = data['room']
    winner_name = data['pick']
    try:
        g = RoomManager.get_game(room_code=room_code)
        g.winner_selected(name=winner_name)
        sio.send(g.serialize(), room=g.room_code)
    except Game.PlayerNotExistsError:
        app.logger.debug(f'Player {winner_name} does not exist')
        sio.emit('error', {'error': f'Player {winner_name} does not exist'})
    except Game.AlreadyWonError:
        app.logger.debug(f'The round has already ended')
        sio.emit('error', {'error': f'The round has already ended'})
    except RoomManager.NoRoomError:
        app.logger.debug(f'Room {room_code} does not exist')
        sio.emit('error', {'error': f'Room {room_code} does not exist.'})


@socket_io_app.on('next')
def on_next(data):
    app.logger.info(data)
    room_code = data['room']
    try:
        g = RoomManager.get_game(room_code=room_code)
        g.next_round()
        sio.send(g.serialize(), room=g.room_code)
        sio.emit('reset', room=g.room_code)
    except RoomManager.NoRoomError:
        app.logger.debug(f'Room {room_code} does not exist')
        sio.emit('error', {'error': f'Room {room_code} does not exist.'})
