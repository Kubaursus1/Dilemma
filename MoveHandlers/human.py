import os
import colorama
from MoveHandlers.playerMoveHandler import PlayerMoveHandler
from MoveResult.baseResult import BaseResult
from card import Card
import game
from suit import Suit
from utis import chooseCardWithKeyboard


class Human(PlayerMoveHandler):
    def _nonActivePlayerChoices(self,lackingSuits) -> tuple[Card, Suit]:
        additionalText = f"{game.getNonActivePlayer()} przekazuje kartę {game.getActivePlayer() if isinstance(self._opponent, Human) else 'Bot,owi'}\n"
        print(additionalText)
        chosenCardByNonActivePlayer = self.showCardsAndCollectInput(game.getNonActivePlayer(), lackingSuits, additionlText=additionalText)

        os.system("cls")   
        print(game)                                 
        activePlayerSuits: list[str] = list(set(map( lambda card : card.getSuit().value, game.getActivePlayer().getHand())))
        additionalText = f"{game.getNonActivePlayer()}, wybierz kształt jaki chcesz otrzymać"
        print(additionalText)
        print(f"[{colorama.Fore.GREEN}{activePlayerSuits[0]}{colorama.Style.RESET_ALL}",", " + ", ".join(str(suit) for suit in activePlayerSuits[1:]) if len(activePlayerSuits) != 1 else "", "]", sep="")
        chosenSuitByNonActivePlayer = chooseCardWithKeyboard(activePlayerSuits, game.getNonActivePlayer(), additionalText=additionalText)
        return (chosenCardByNonActivePlayer, chosenSuitByNonActivePlayer)

    def _handleExchangeMove(self) -> BaseResult:
        lackingSuits = self.lackingSuitsCalculator()
        chosenCardByNonActivePlayer, chosenSuitByNonActivePlayer  = self._opponent._nonActivePlayerChoices(lackingSuits)
                        
        os.system("cls")
        print(game)
        additionalText = f"{game.getActivePlayer()}, przekaż kartę {game.getNonActivePlayer()} z kształtu jaki chce otrzymać"
        print(additionalText)
        chosenCardByActivePlayer = self.showCardsAndCollectInput(game.getActivePlayer(), set(chosenSuitByNonActivePlayer), additionlText=additionalText)
        
        return game.tryExchangeAndPlaceCardByActivePlayer(chosenCardByActivePlayer, chosenCardByNonActivePlayer)
            
    def _handlePlaceCardMove(self)-> BaseResult:       
        allSuits = set(e.value for e in Suit)
        card = self.showCardsAndCollectInput(game.getActivePlayer(),allSuits)

        return game.tryPlaceCardByActivePlayer(card)
