from datetime import datetime
import flask_socketio as sio
import json
import gc
from os.path import join, abspath, dirname
import random
import string
import time

APP_ROOT = abspath(join(dirname(__file__), ".."))


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
    def create_game(cls, first_player_name):
        room_code = cls.generate_room_code()
        g = Game(room_code)
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
        self.score = 0
        self.hand = dict.fromkeys(initial_cards)
        self.selected_card = ""

    def serialize(self):
        return self.__dict__

    def get_card_list(self):
        return list(self.hand.keys())


class Deck:
    def __init__(self, card_list=[]):
        self.cards = card_list
        self.discarded = []

    def draw(self, n):
        if 1 <= n <= len(self.cards):
            ret = self.cards[-n:]
            del self.cards[-n:]
            return ret
        return []

    def shuffle(self):
        random.shuffle(self.cards)

    def discard(self, card_list):
        self.discarded.extend(card_list)


class Game:
    def __init__(self, room_code):
        self.room_code = room_code
        self.players = {}  # player_name: Player()
        self.dealer = ""
        self.date_created = datetime.now()
        self.date_modified = self.date_created
        self.submissions = {}

        self.white_deck, self.black_deck = self.load_cards(join(APP_ROOT, "card_data", "base.json"))
        self.white_deck.shuffle()
        self.black_deck.shuffle()
        self.current_black_card = self.black_deck.draw(n=1)[0]

    def serialize(self):
        return {
            "room_code": self.room_code,
            "players": {name: player.serialize() for name, player in self.players.items()},
            "dealer": self.dealer,
            "black_card": self.current_black_card,
            "date_created": str(self.date_created),
            "date_modified": str(self.date_modified),
            "playtime": self.playtime(),
        }

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

    def playtime(self):
        fmt = '%Y-%m-%d %H:%M:%S'  # 2018-08-12 10:12:25.700528
        d1 = self.date_created
        d2 = self.date_modified
        # Convert to Unix timestamp
        d1_ts = time.mktime(d1.timetuple())
        d2_ts = time.mktime(d2.timetuple())
        return round(float(d2_ts-d1_ts) / 60, 2)

    @staticmethod
    def load_cards(path):
        with open(path, 'r') as f:
            json_data = json.load(f)
        return Deck(json_data['whiteCards']), Deck(json_data['blackCards'])


if __name__ == "__main__":
    white, black = Game.load_cards("card_data/base.json")
    print("got here")
