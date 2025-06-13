import copy
import uuid
from card import Card
from cardscollection import CardsCollection
from utis import is_valid_uuid

class Player(CardsCollection):
    def __init__(self, name:str):
        self.__name = name
        self.__score = 0
        self.__hand = []
        
    def add(self,card:Card):
        self.__hand.append(card)
    def remove(self,card:Card):
        self.__hand.remove(card)
        
    def getHand(self) -> list[Card]:
        # zeby nie mozna bylo zmienic zawartosci listy kart
        return copy.copy(self.__hand)
    
    def __repr__(self) -> str:
        return self.__name if not is_valid_uuid(self.__name) else "Bot"
    
    def assignScore(self, trick):
        last_card = trick.last()
        self.__score += last_card.getRank().value
    
    def getName(self):
        return self.__name
    
    def getScore(self):
        return self.__score