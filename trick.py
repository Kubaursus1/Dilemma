import copy
from move import PlaceCardMove
from cardsTransfer import transferCard
from MoveResult.baseResult import BaseResult
from MoveResult.errorResult import SuitDuplicated
from MoveResult.okResult import * 
from card import Card
from cardscollection import CardsCollection

class Trick(CardsCollection):
    max_size = 4
    
    def __init__(self):
        self.__cards:list[Card] = []
       
    def isSuitDuplicated(self, card:Card):
        for c in self.__cards:
            if c.getSuit() == card.getSuit():
                return True
        return False
    def add(self,card:Card):
        if len(self.__cards) >= Trick.max_size:
            raise RuntimeError("Trick is already full")
        if self.isSuitDuplicated(card):
            raise RuntimeError("Trick has already a card with this suit!")
                                         
        self.__cards.append(card)
    def remove(self,card:Card):
        raise RuntimeError("Operation is not supported")
    def isFull(self) -> bool:
        return len(self.__cards) == Trick.max_size
    def __repr__(self) -> str:
        return str(self.__cards)
    def len(self) -> int:
        return len(self.__cards)
    def last(self)->Card:
        return self.__cards[-1]
    def first(self)->Card:
        return self.__cards[0]
    def getCardsByIndexes(self,indexes:list[int]) -> list[Card]:
        result = []
        for i in indexes:
            result.append(self.__cards[i])
        return result
    def getAllCards(self)-> list[Card]: 
        return copy.deepcopy(self.__cards)
    
class Tricks:    
    def __init__(self):
        self.__tricks:list[Trick] = [Trick()]
    
    def __addNewTrickIfShould(self):
        if self.getCurrentTrick().isFull():
            self.__tricks.append(Trick())
    
    def getCurrentTrick(self)->Trick:
        return self.__tricks[-1]
    
    def getTricks(self)->list[Trick]:
        return copy.deepcopy(self.__tricks)
    
    def tryPlaceCard(self,move:PlaceCardMove)->BaseResult:
        self.__addNewTrickIfShould()
        currentTrick = self.getCurrentTrick()
        if currentTrick.isSuitDuplicated(move.card):
            return SuitDuplicated()
        
        transferCard(move.card,move.player, currentTrick)       
        
        if currentTrick.isFull():
            return TrickCompleted(currentTrick)
        
        return TrickNotCompleted(currentTrick)
    
    def __repr__(self) -> str:
        return str(self.getCurrentTrick())