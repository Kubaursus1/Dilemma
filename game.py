from typing import Callable, Optional
import uuid
from move import PlaceCardMove
from MoveResult.baseResult import BaseResult
from card import Card
from cardsTransfer import transferCard, transferCards
from trick import Tricks
from trick import Trick
from deck import Deck
from player import Player
from gameState import GameState, GameResult

class Game:                    
    class GameProxy:
        cardsToDraw = 4         
        def __init__(self, game:"Game"):
            self.game=game
        
        def tryRestoreCards(self):
            if (self.canRestoreCards()):                      
                self.restorePlayersCards()   
            elif not (self.canRestoreCards()) and len(self.game.getNonActivePlayer().getHand()) == 0:
                self.game._Game__startNewDeck()
        def restorePlayersCards(self):       
            cards = self.game.getDeck().getTopCards(Game.GameProxy.cardsToDraw)
            transferCards(cards[:2], self.game.getDeck(), self.game.getTrickLeader())
            transferCards(cards[2:], self.game.getDeck(), self.game.getTrickNonLeader())
                
        def updateLeader(self, new_leader:Player):
            if new_leader == self.game._Game__leader: # type: ignore
                return
            self.swapLeader()            
                        
        def swapLeader(self):
            self.game._Game__leader, self.game._Game__nonLeader = self.game._Game__nonLeader,self.game._Game__leader # type: ignore
            
        def updateActivePlayer(self) ->Player:                
            currentTrick = self.game.getTricks().getCurrentTrick()
            if(currentTrick.isFull()):
                self.game._Game__activePlayer = self.game._Game__leader # type: ignore                
            elif not(currentTrick.len() == 2 and currentTrick.last().getRank().value > currentTrick.first().getRank().value):                    
                self.game._Game__swapActivePlayer() # type: ignore
            return self.game._Game__activePlayer  # type: ignore
        def getTrickWinner(self) -> Player:
            return self.game._Game__getTrickWinner() # type: ignore
        def canRestoreCards(self):
            return self.game.getDeck().size() >= Game.GameProxy.cardsToDraw
        def setActivePlayerCanNotPlaceCard(self, activePlayerCanNotPlaceCard:bool):
            self.game._Game__activePlayerCanNotPlaceCard = activePlayerCanNotPlaceCard # type: ignore
    
    fullHandSize = 5
    winningScore = 100
        
    def __init__(self, firstPlayerName:str,secondPlayerName:str):
       self.__firtsName =  firstPlayerName
       self.__secondName = secondPlayerName
       self.__gameState = GameState.NOT_STARTED      
       self.__activePlayerCanNotPlaceCard = False 
       self.__proxy = Game.GameProxy(self)
    
    def startNewDealAndStartGame(self):
        self.__leader = Player(self.__firtsName)
        self.__nonLeader = Player(self.__secondName)
        self.__activePlayer = self.__leader
        
        self.__gameState = GameState.STARTED
        
        self.__tricks = Tricks()
        
        self.__startNewDeck()
    
    def __startNewDeck(self):
        self.__deck = Deck()
        self.__deck.shuffle()
        
        for _ in range(Game.fullHandSize):
            transferCard(self.__deck.getTopCard(), self.__deck,self.__leader)
            transferCard(self.__deck.getTopCard(), self.__deck,self.__nonLeader)
             
    def __getTrickWinner(self) -> Player:
        def calcScore(cards:list[Card],elemFun:Callable[[int, int], int],initValue:int) -> int:              
            acc = initValue
            for c in cards:
                acc = elemFun(acc,c.getRank().value)
            return acc
        def getFirstMaxCardIndex(currentTrick:Trick)->int:
            maxIndex = 0
            cards = currentTrick.getAllCards()[1:]
            for idx,card in enumerate(cards):
                if card.getRank().value > cards[maxIndex].getRank().value:
                    maxIndex = idx
            return maxIndex
        
        (leaderCardsIdx,nonLeaderCardsIdx) = ([0,3],[1,2]) if self.__activePlayer == self.__leader  else ([0,2],[1,3])
        curTrick = self.getTricks().getCurrentTrick()
        (leaderCards,nonLeaderCards) = (curTrick.getCardsByIndexes(leaderCardsIdx),
                                        curTrick.getCardsByIndexes(nonLeaderCardsIdx))
        def add (a, b):
            return a + b 
        def mul(a,b):
            return a*b
        
        (leaderScore,nonLeaderScore) = (calcScore(leaderCards,add,0),
                                        calcScore(nonLeaderCards,add,0))        
        if leaderScore != nonLeaderScore:
            return self.__leader if leaderScore > nonLeaderScore else self.__nonLeader
                    
        (leaderScore,nonLeaderScore) = (calcScore(leaderCards,mul,1),
                                        calcScore(nonLeaderCards,mul,1))            
        if leaderScore != nonLeaderScore:
            return self.__leader if leaderScore > nonLeaderScore else self.__nonLeader
        
        maxIndex = getFirstMaxCardIndex(curTrick)
        return self.__leader if maxIndex in leaderCardsIdx else self.__nonLeader
                      
    def __swapActivePlayer(self):        
        self.__activePlayer = self.__nonLeader if self.__leader == self.__activePlayer else self.__leader
    
    def tryExchangeAndPlaceCardByActivePlayer (self,activePlayerCard:Card,nonActivePlayerCard:Card)->BaseResult:
        if not self.__activePlayerCanNotPlaceCard:
            raise RuntimeError("Standard moves are possible. Use tryPlaceCardByActivePlayer")    
        if self.__gameState != GameState.STARTED:
            raise RuntimeError("Game is not in started state")            
        if activePlayerCard not in self.__activePlayer.getHand(): 
            raise ValueError("Invalid card owner","activePlayerCard")
        if nonActivePlayerCard not in self.getNonActivePlayer().getHand(): 
            raise ValueError("Invalid card owner","nonActivePlayerCard")
        
        currentTrick = self.__tricks.getCurrentTrick()
        if currentTrick.isSuitDuplicated(nonActivePlayerCard):
            raise ValueError("Non active player card is not valid, cannot be placed in trick")
        
        transferCard(nonActivePlayerCard, self.getNonActivePlayer(), self.__activePlayer)
        transferCard(activePlayerCard, self.__activePlayer, self.getNonActivePlayer())
          
        self.__activePlayerCanNotPlaceCard = False                
        return self.tryPlaceCardByActivePlayer(nonActivePlayerCard)        
        
    def tryPlaceCardByActivePlayer(self,card:Card)->BaseResult:
        if self.__gameState != GameState.STARTED:
            raise RuntimeError("Game is not in started state")
        if self.__activePlayerCanNotPlaceCard:
            raise RuntimeError("No moves possible, in this state You must only call 'tryExchangeAndPlaceCardByActivePlayer' method")            
        if card not in self.__activePlayer.getHand(): 
            raise ValueError("Invalid card owner",f"{card}")
        
        result = self.__tricks.tryPlaceCard(PlaceCardMove(self.__activePlayer,card))               
        result.handle(self.__proxy)
        
        if self.tryGetGameResult() is not None:
            self.__finishGame()                           
        
        return result
            
    def __finishGame(self):
        self.__gameState = GameState.ENDED
    def tryGetGameResult(self)->Optional[GameResult]:
        isSecendPlayerWinner = self.getPlayerByName(self.__secondName).getScore() >= Game.winningScore
        isFirstPlayerWinner = self.getPlayerByName(self.__firtsName).getScore() >= Game.winningScore
        if isFirstPlayerWinner:
            return GameResult.WINNER_FIRST
        elif isSecendPlayerWinner:
            return GameResult.WINNER_SECOND
        elif isFirstPlayerWinner and isSecendPlayerWinner:
            return GameResult.DRAW
        else:
            return None
    def getGameResult(self)->GameResult:
        res = self.tryGetGameResult()
        if res is not None:
            return res
        raise ValueError("Game is not in proper state")        
    def getActivePlayer(self)->Player:
        return self.__activePlayer
    def getNonActivePlayer(self)->Player:
        return self.__leader if self.__nonLeader == self.__activePlayer else self.__nonLeader
    def getPlayers(self)->list[Player]:
        return [self.__leader,self.__nonLeader]
    def getPlayerByName(self, name) -> Player:
        if self.__leader.getName() == name:
            return self.__leader
        elif self.__nonLeader.getName() == name:
            return self.__nonLeader
        else:
            raise ValueError("Player does not exist")
    def getFirstPlyerName(self):
        return self.__firtsName
    def getSecondPlayerName(self):
        return self.__secondName
    def getActivePlayerCanNotPlaceCard(self) -> bool:
        return self.__activePlayerCanNotPlaceCard
    def getDeck(self) -> Deck:
        return self.__deck
    def getTrickLeader(self) -> Player:
        return self.__leader
    def getTrickNonLeader(self) -> Player:
        return self.__nonLeader
    def getGameState(self) -> GameState:
        return self.__gameState
    def __repr__(self) -> str:
        return f" State: {self.__gameState} \n Deck: {self.__deck}\n Tricks: {self.__tricks} \n Leader: {self.__leader} \n Non-leader: {self.__nonLeader} \nActive: {self.__activePlayer.getName()} "    
    def __str__(self) -> str:
        return f" Tricks: {self.__tricks} \n {self.__firtsName}: {self.getPlayerByName(self.__firtsName).getScore()} \n {self.__secondName if not isinstance(self.__secondName, uuid.UUID) else 'Bot'}: {self.getPlayerByName(self.__secondName).getScore()} "    
    def getTricks(self) ->Tricks:
        return self.__tricks