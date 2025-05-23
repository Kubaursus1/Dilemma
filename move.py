from card import Card
from player import Player

class Move:
    pass

class PlaceCardMove(Move):
    def __init__(self, player:Player, card:Card):
        self.player = player
        self.card = card