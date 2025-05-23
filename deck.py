import random
from suit import Suit
from rank import Rank
from card import Card
from cardscollection import CardsCollection

class Deck(CardsCollection):
    def __init__(self):
        self.__cards = []
        for suit in Suit:
            for rank in Rank:
                self.__cards.append(Card(suit,rank))
    def shuffle(self):
        random.shuffle(self.__cards)        
    def add(self,card):
        self.__cards.append(card)
    def remove(self,card):
        self.__cards.remove(card)        
    def isEmpty(self)->bool:        
        return len(self.__cards) == 0
    def getTopCard(self)->Card:
        return self.getTopCards(1)[0]     
    def getTopCards(self, cardsCount) -> list[Card]: 
        if len(self.__cards) < cardsCount:
            raise RuntimeError("Not enought cards in deck")
        return self.__cards[0:cardsCount]
    def size(self) -> int:
        return len(self.__cards)
    def __repr__(self) -> str:
        return str(self.__cards)