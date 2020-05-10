from sys import getsizeof

from flask import Blueprint, request, jsonify
import flask_socketio as sio

from app import socket_io_app, app
from app.cah.game import RoomManager, Game
from app.cah.card_data import Deck

cah_bp = Blueprint('cah', __name__,
                   url_prefix='',
                   static_url_path='',
                   static_folder='./dist/static/',
                   template_folder='./dist/',
                   )


@app.route('/info')
def stats():
    resp = {
        'numRooms': len(RoomManager.rooms),
        'totalPlayers': sum(len(g.players) for g in RoomManager.rooms.values()),
        'bytesUsed': getsizeof(RoomManager.rooms),
        'rooms': {k: v.summary() for k, v in RoomManager.rooms.items()}
    }
    return jsonify(resp)


@socket_io_app.on('list_decks')
def on_list_decks():
    app.logger.debug("")
    deck_list = Game.CARD_DATA.get_deck_list()
    sio.emit('list_decks', {'deck_list': deck_list})
    RoomManager.prune()


@socket_io_app.on('create')
def on_create(data):
    app.logger.debug(data)
    try:
        g = RoomManager.create_game(first_player_name=data['username'], deck_code_list=data['decks'])
        app.logger.debug(f'Created game with room code {g.room_code}')
        sio.join_room(g.room_code)
        sio.send(g.serialize(), room=g.room_code)
        RoomManager.prune()
    except Deck.InsufficientCardsError:
        app.logger.debug(f'Insufficient cards in game')
        sio.emit('error', {'error': f'Insufficient cards in game.'})


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
    except Deck.InsufficientCardsError:
        app.logger.debug(f'Insufficient cards in game another player')
        sio.emit('error', {'error': f'Insufficient cards in game for another player.'})


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


@socket_io_app.on('vote')
def on_vote(data):
    app.logger.info(data)
    room_code = data['room']
    voter = data['voter']
    vote_receiver = data['vote_receiver']
    try:
        g = RoomManager.get_game(room_code=room_code)
        g.add_vote(voter=voter, vote_receiver=vote_receiver)
        sio.send(g.serialize(), room=g.room_code)
    except Game.PlayerNotExistsError:
        app.logger.debug(f'Player does not exist')
        sio.emit('error', {'error': f'Player does not exist'})
    except Game.AlreadyEndedError:
        app.logger.debug(f'The round has already ended')
        sio.emit('error', {'error': f'The round has already ended'})
    except RoomManager.NoRoomError:
        app.logger.debug(f'Room {room_code} does not exist')
        sio.emit('error', {'error': f'Room {room_code} does not exist.'})
    except Game.AlreadyVotedError:
        app.logger.debug(f'Player {voter} has already voted')
        sio.emit('error', {'error': f'You have already voted'})


@socket_io_app.on('end')
def on_end(data):
    app.logger.info(data)
    room_code = data['room']
    try:
        g = RoomManager.get_game(room_code=room_code)
        g.end_round()
        sio.send(g.serialize(), room=g.room_code)
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
        sio.emit('next', room=g.room_code)
    except RoomManager.NoRoomError:
        app.logger.debug(f'Room {room_code} does not exist')
        sio.emit('error', {'error': f'Room {room_code} does not exist.'})
