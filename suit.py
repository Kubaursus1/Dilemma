from enum import Enum

class Suit(Enum):
    SPADES = '♣'
    DIAMONS = '♦'
    HEARTS = '♥'
    CLUBS = '♠'
   
    
    def __init__(self, symbol):
        self.__symbol = symbol    
    def getSymbol(self):
        return self.__symbol
    def __str__(self) -> str:
        return self.__symbol