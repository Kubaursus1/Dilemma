from suit import Suit
from rank import Rank

class Card:
    def __init__(self, suit:Suit, rank:Rank):
        self.__suit = suit
        self.__rank = rank
    def __repr__(self) -> str:
        return f"{str(self.__suit.getSymbol())} {str(self.__rank.value)}"
    def getSuit(self)->Suit:
        return self.__suit
    def getRank(self) -> Rank:
        return self.__rank