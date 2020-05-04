from datetime import datetime
import flask_socketio as sio
import gc
import os
import random
import string
import time

from app.cah.card_data import CardData


class RoomManager:
    rooms = {}

    class NoRoomError(Exception):
        pass

    @classmethod
    def get_game(cls, room_code):
        if room_code in cls.rooms:
            return cls.rooms[room_code]
        raise RoomManager.NoRoomError

    @staticmethod
    def generate_room_code():
        id_length = 5
        return ''.join(random.SystemRandom().choice(
            string.ascii_uppercase) for _ in range(id_length))

    @classmethod
    def create_game(cls, first_player_name, deck_code_list):
        room_code = cls.generate_room_code()
        g = Game(room_code=room_code, deck_code_list=deck_code_list)
        g.dealer = first_player_name
        g.add_player(first_player_name)
        cls.rooms[room_code] = g
        return g

    @classmethod
    def prune(cls):
        def is_stale(room):
            """Stale rooms are older than 6 hours, or have gone 20 minutes less than 5 minutes of total playtime"""
            return (((datetime.now() - room.date_modified).total_seconds() >= (60*60*24)) or
                    ((datetime.now() - room.date_modified).total_seconds() >= (60*20) and
                     room.playtime() <= 5))

        for room_code in cls.rooms.keys():
            if is_stale(cls.rooms[room_code]):
                sio.close_room(room_code)
                cls.rooms.pop(room_code, None)
        gc.collect()


class Player:
    def __init__(self, name, initial_cards):
        self.name = name
        self.roundsWon = 0
        self.hand = dict.fromkeys(initial_cards)
        self.submission = ""
        self.submissionRevealed = False
        self.hasSubmitted = False
        self.submissionNumber = 0
        self.isWinner = False
        self.submittedCards = []
        self.hasVoted = False
        self.votes = 0

    def serialize(self):
        return self.__dict__

    def get_card_list(self):
        return list(self.hand.keys())

    def end_round(self, deck):
        if self.hasSubmitted:
            for card in self.submittedCards:
                self.hand.pop(card)
            self.hand.update(
                dict.fromkeys(
                    deck.draw(len(self.submittedCards))))
            deck.discard(self.submittedCards)
        self.submittedCards = []
        self.submission = ""
        self.submissionRevealed = False
        self.hasSubmitted = False
        self.submissionNumber = 0
        self.isWinner = False
        self.hasVoted = False
        self.votes = 0


class Game:
    app_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    CARD_DATA = CardData(path=os.path.join(app_root, "card_data", "official.json"))

    def __init__(self, room_code, deck_code_list):
        self.room_code = room_code
        self.players = {}  # player_name: Player()
        self.dealer = ""
        self.date_created = datetime.now()
        self.date_modified = self.date_created
        self.submissionNumber = 0
        self.round_ended = False
        self.rounds_played = 0

        self.black_deck, self.white_deck = Game.CARD_DATA.get_decks(deck_code_list)
        self.black_deck.shuffle()
        self.white_deck.shuffle()
        self.current_black_card = self.black_deck.draw(n=1)[0]

    def serialize(self):
        ret = {
            "room_code": self.room_code,
            "players": {name: player.serialize() for name, player in self.players.items()},
            "dealer": self.dealer,
            "black_card": self.current_black_card,
            "date_created": str(self.date_created),
            "date_modified": str(self.date_modified),
            "playtime": self.playtime(),
            "rounds_played": self.rounds_played,
            "round_ended": self.round_ended
        }
        import pprint as pp
        pp.pprint(ret)
        return ret

    class PlayerExistsError(Exception):
        pass

    def add_player(self, name):
        if name in self.players:
            raise Game.PlayerExistsError
        p = Player(name=name, initial_cards=self.white_deck.draw(10))
        self.players[name] = p
        return p

    def remove_player(self, name):
        if name in self.players:
            p = self.players[name]
            self.white_deck.discard(p.get_card_list())  # Return cards to discard pile
            self.players.pop(name, None)

    class PlayerNotExistsError(Exception):
        pass

    class PlayerAlreadySubmittedError(Exception):
        pass

    def add_submission(self, player_name, submission, submitted_cards):
        if player_name not in self.players:
            raise Game.PlayerNotExistsError
        p = self.players[player_name]
        if p.hasSubmitted:
            raise Game.PlayerAlreadySubmittedError
        p.submission = submission
        p.submittedCards = submitted_cards
        p.hasSubmitted = True
        p.submissionNumber = self.submissionNumber
        self.submissionNumber += 1

    def reveal_submission(self, player_name):
        if player_name not in self.players:
            raise Game.PlayerNotExistsError
        p = self.players[player_name]
        p.submissionRevealed = True

    class AlreadyEndedError(Exception):
        pass

    class AlreadyVotedError(Exception):
        pass

    def add_vote(self, voter, vote_receiver):
        if voter not in self.players or vote_receiver not in self.players:
            raise Game.PlayerNotExistsError
        if self.round_ended:
            raise Game.AlreadyEndedError

        v = self.players[voter]
        if v.hasVoted:
            raise Game.AlreadyVotedError
        v.hasVoted = True

        p = self.players[vote_receiver]
        p.votes += 1

    def end_round(self):
        self.round_ended = True
        max_votes = max(player.votes for player in self.players.values())
        for name, player in self.players.items():
            if player.votes == max_votes and player.votes > 0:
                player.roundsWon += 1
                player.isWinner = True

    def next_round(self):
        self.round_ended = False
        self.submissionNumber = 0
        self.rounds_played += 1

        # Put used cards in discard piles
        for name, player in self.players.items():
            player.end_round(self.white_deck)
        self.black_deck.discard(self.current_black_card)
        self.current_black_card = self.black_deck.draw(1)[0]

        # Select the next dealer
        if len(self.players) > 1:
            names = list(self.players.keys())
            self.dealer = names[(names.index(self.dealer) + 1) % len(names)]

    def playtime(self):
        fmt = '%Y-%m-%d %H:%M:%S'  # 2018-08-12 10:12:25.700528
        d1 = self.date_created
        d2 = self.date_modified
        # Convert to Unix timestamp
        d1_ts = time.mktime(d1.timetuple())
        d2_ts = time.mktime(d2.timetuple())
        return round(float(d2_ts-d1_ts) / 60, 2)

