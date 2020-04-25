from datetime import datetime
from functools import singledispatch
import json
from os.path import join, abspath, dirname
import random
import string
import time

APP_ROOT = abspath(join(dirname(__file__), ".."))


class Player:
    def __init__(self, name, initial_cards):
        self.name = name
        self.score = 0
        self.hand = dict.fromkeys(initial_cards)
        self.selected_card = ""

    def to_serializable(self):
        return self.__dict__


class CardDeck:
    def __init__(self, card_list):
        self.cards = card_list

    def draw(self, n):
        if 1 <= n <= len(self.cards):
            ret = self.cards[-n:]
            del self.cards[-n:]
            return ret
        return []


class GameState:
    def __init__(self):
        self.game_id = self.generate_room_id()
        self.players = {}  # player_name: Player()
        self.dealer = ""
        self.date_created = datetime.now()
        self.date_modified = self.date_created
        self.white_deck, self.black_deck = self.load_cards(join(APP_ROOT, "card_data", "base.json"))

        # TODO: Randomize card order

    @classmethod
    def from_first_player(cls, first_player_name):
        gs = cls()
        gs.dealer = first_player_name
        gs.players = {
            first_player_name: Player(name=first_player_name,
                                      initial_cards=gs.white_deck.draw(10))
        }
        return gs

    def to_serializable(self):
        return {
            "game_id": self.game_id,
            "players": {name: player.to_serializable() for name, player in self.players.items()},
            "dealer": self.dealer,
            "date_created": str(self.date_created),
            "date_modified": str(self.date_modified),
            "playtime": self.playtime(),
        }

    def add_player(self, name):
        pass

    def remove_player(self, name):
        pass

    @staticmethod
    def generate_room_id():
        """Generate a random room ID"""
        id_length = 5
        return ''.join(random.SystemRandom().choice(
            string.ascii_uppercase) for _ in range(id_length))

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
        return CardDeck(json_data['whiteCards']), CardDeck(json_data['blackCards'])


if __name__ == "__main__":
    x = GameState.from_first_player(first_player_name="john")
    json.dumps(x.to_serializable())
    print("asdf")