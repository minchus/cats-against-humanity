import json
import random


class Deck:
    def __init__(self, card_list=None):
        if card_list is None:
            card_list = []
        self.cards = card_list
        self.discarded = []

    class InsufficientCardsError(Exception):
        pass

    def draw(self, n):
        # If too few cards remaining in deck try and re-use discarded
        if n > len(self.cards):
            self.cards.extend(self.discarded)
            self.discarded = []
            self.shuffle()

        if n > len(self.cards):
            raise Deck.InsufficientCardsError

        if n >= 1:
            ret = self.cards[-n:]
            del self.cards[-n:]
            return ret
        return []

    def shuffle(self):
        random.shuffle(self.cards)

    def discard(self, card_list):
        self.discarded.extend(card_list)


class CardData:
    def __init__(self, path):
        with open(path, 'r') as f:
            self.json_data = json.load(f)

        self.deck_list = []
        code_list = self.json_data['order']
        for code in code_list:
            deck_info = self.json_data[code]
            name = deck_info['name']
            num_black_cards = len(deck_info['black'])
            num_white_cards = len(deck_info['white'])
            description = f'{name} ({num_black_cards} black, {num_white_cards} white)'
            self.deck_list.append({'code': code, 'description': description})

    def get_deck_list(self):
        return self.deck_list

    def get_decks(self, code_list):
        black_card_indexes = []
        white_card_indexes = []
        for code in code_list:
            black_card_indexes.extend(self.json_data[code]['black'])
            white_card_indexes.extend(self.json_data[code]['white'])

        black_cards = [self.json_data['blackCards'][i] for i in black_card_indexes]
        white_cards = [self.json_data['whiteCards'][i] for i in white_card_indexes]
        return Deck(black_cards), Deck(white_cards)
