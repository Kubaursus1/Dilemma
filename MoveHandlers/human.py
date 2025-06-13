import os
import colorama
from MoveHandlers.playerMoveHandler import PlayerMoveHandler
from MoveResult.baseResult import BaseResult
from card import Card
from suit import Suit
from utis import chooseCardWithKeyboard


class Human(PlayerMoveHandler):
    def _nonActivePlayerChoices(self,lackingSuits:set[str]) -> tuple[Card, Suit]:
        additionalText = f"{self._game.getNonActivePlayer()} przekazuje kartę {self._game.getActivePlayer() if isinstance(self._opponent, Human) else 'Bot,owi'}\n"
        print(additionalText)
        chosenCardByNonActivePlayer = self.showCardsAndCollectInput(self._game.getNonActivePlayer(), lackingSuits, additionlText=additionalText)

        os.system("cls")   
        print(self._game)                                 
        activePlayerSuits: list[str] = list(set(map( lambda card : card.getSuit().value, self._game.getActivePlayer().getHand())))
        additionalText = f"{self._game.getNonActivePlayer()}, wybierz kształt jaki chcesz otrzymać"
        print(additionalText)
        print(f"[{colorama.Fore.GREEN}{activePlayerSuits[0]}{colorama.Style.RESET_ALL}",", " + ", ".join(str(suit) for suit in activePlayerSuits[1:]) if len(activePlayerSuits) != 1 else "", "]", sep="")
        chosenSuitByNonActivePlayer = chooseCardWithKeyboard(self._game,activePlayerSuits, self._game.getNonActivePlayer(), additionalText=additionalText)
        return (chosenCardByNonActivePlayer, chosenSuitByNonActivePlayer)

    def _handleExchangeMove(self ) -> BaseResult:
        lackingSuits = self.lackingSuitsCalculator(self._game)
        chosenCardByNonActivePlayer, chosenSuitByNonActivePlayer  = self._opponent._nonActivePlayerChoices(lackingSuits, self._game)
                        
        os.system("cls")
        print(self._game)
        additionalText = f"{self._game.getActivePlayer()}, przekaż kartę {self._game.getNonActivePlayer()} z kształtu jaki chce otrzymać"
        print(additionalText)
        chosenCardByActivePlayer = self.showCardsAndCollectInput(self._game.getActivePlayer(), set(chosenSuitByNonActivePlayer), additionlText=additionalText)
        
        return self._game.tryExchangeAndPlaceCardByActivePlayer(chosenCardByActivePlayer, chosenCardByNonActivePlayer)
            
    def _handlePlaceCardMove(self )-> BaseResult:       
        allSuits = set(e.value for e in Suit)
        card = self.showCardsAndCollectInput(self._game.getActivePlayer(),allSuits)

        return self._game.tryPlaceCardByActivePlayer(card)
