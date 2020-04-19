"""Object for tracking game status"""
from datetime import datetime
import json
from os.path import join, abspath, dirname
import random
import string
import time

APP_ROOT = abspath(join(dirname(__file__), ".."))


class Player:
    def __init__(self, name, is_dealer):
        self.name = name
        self.hand = []
        self.is_dealer = is_dealer
        self.score = 0


class GameState:
    def __init__(self):
        self.game_id = self.generate_room_id()
        self.date_created = datetime.now()
        self.date_modified = self.date_created
        self.players = {}

        self.white_cards, self.black_cards = self.load_card_data(join(APP_ROOT, "card_data", "base.json"))

    def to_json(self):
        """Serialize object to JSON"""
        return {
            "game_id": self.game_id,
            "players": self.players,
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
    def load_card_data(path):
        with open(path, 'r') as f:
            json_data = json.load(f)
        return json_data['blackCards'], json_data['whiteCards']


if __name__ == "__main__":
    tmp = GameState()
    print("asdf")