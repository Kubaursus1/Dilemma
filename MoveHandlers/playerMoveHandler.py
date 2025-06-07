import time
import colorama
from MoveResult.baseResult import BaseResult
from card import Card
from game import Game
from player import Player
from suit import Suit
from utis import chooseCardWithKeyboard


class PlayerMoveHandler:
    def __init__(self, name):
        self._name = name
        
    def setOpponent(self,opponent:"PlayerMoveHandler"):
        self._opponent = opponent        
        
    def showCardsAndCollectInput(self, targetPlayer: Player, suits: set[str],game:Game, additionlText=None) -> Card: 
        print(f"{targetPlayer.getName()}, wybierz kartę.")
            
        cards = list(filter(lambda card : card.getSuit().value in suits, targetPlayer.getHand()))
        print(f"[{colorama.Fore.GREEN}{cards[0]}{colorama.Style.RESET_ALL}",", " + ", ".join(str(card) for card in cards[1:]) if len(cards) != 1 else "", "]", sep="")
        return chooseCardWithKeyboard(cards, targetPlayer, game, additionalText=additionlText if additionlText !=None else None)
    def lackingSuitsCalculator(self, game:Game) -> set[str]:
        trickSuits = set(map( lambda card : card.getSuit().value, game.getTricks().getCurrentTrick().getAllCards()))
        allSuits = set(e.value for e in Suit)
        lackingSuits = allSuits-trickSuits
        return lackingSuits
  
    def cardChoosingAnimation(self, animationTimesCount: int):
        for _ in range(animationTimesCount):
            for i in ["|", "/", "-", "\\"]:
                print(f"\r{i}", end="")
                time.sleep(0.15)  
    
    def handlePlayerMove(self,game:Game)-> BaseResult:
        return self._handleExchangeMove(game) if game.getActivePlayerCanNotPlaceCard() else self._handlePlaceCardMove(game)
        
    def _handlePlaceCardMove(self, game:Game) -> BaseResult:
        pass
        
    def _handleExchangeMove(self, game:Game) -> BaseResult:
        pass

    def _nonActivePlayerChoices(self,lackingSuits: set[str], game:Game) -> tuple[Card, Suit]:
        pass
                  