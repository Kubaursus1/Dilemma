from suit import Suit
from MoveResult.baseResult import BaseResult

class OkResult(BaseResult):
    def handle(self,game)->None:        
        pass
        
class TrickCompleted(OkResult):
    def __init__(self,trick):
        self.trick = trick
    def handle(self,game)->None:        
        winner = game.getTrickWinner()      
        winner.assignScore(self.trick)
        
        game.tryRestoreCards()                
        game.updateLeader(winner)                
        game.updateActivePlayer()
                         
class TrickNotCompleted(OkResult):
    def __init__(self,trick):      
        self.trick = trick
    
    def __isNextMovePossible(self,player) -> bool:
     
        handSuits = set(map( lambda card : card.getSuit().value, player.getHand()))
        trickSuits = set(map( lambda card : card.getSuit().value, self.trick.getAllCards()))
        allSuits = set(e.value for e in Suit)
        
        return bool((allSuits - trickSuits) & handSuits) 
                    
    def handle(self,game)->None:                
        activePlayer = game.updateActivePlayer()        
        game.setActivePlayerCanNotPlaceCard(not self.__isNextMovePossible(activePlayer))
   