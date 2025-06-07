import os
import colorama
from MoveHandlers.playerMoveHandler import PlayerMoveHandler
from MoveResult.baseResult import BaseResult
from card import Card
from game import Game
from suit import Suit
from utis import chooseCardWithKeyboard


class Human(PlayerMoveHandler):
    def _nonActivePlayerChoices(self,lackingSuits: set[str], game:Game) -> tuple[Card, Suit]:
        additionalText = f"{game.getNonActivePlayer()} przekazuje kartę {game.getActivePlayer() if isinstance(self._opponent, Human) else "Bot'owi"}\n"
        print(additionalText)
        chosenCardByNonActivePlayer = self.showCardsAndCollectInput(game.getNonActivePlayer(), lackingSuits, game, additionlText=additionalText)

        os.system("cls")   
        print(game)                                 
        activePlayerSuits: list[str] = list(set(map( lambda card : card.getSuit().value, game.getActivePlayer().getHand())))
        additionalText = f"{game.getNonActivePlayer() if isinstance(self._opponent, Human) else "Bot'owi"}, wybierz kształt jaki chcesz otrzymać"
        print(additionalText)
        print(f"[{colorama.Fore.GREEN}{activePlayerSuits[0]}{colorama.Style.RESET_ALL}",", " + ", ".join(str(suit) for suit in activePlayerSuits[1:]) if len(activePlayerSuits) != 1 else "", "]", sep="")
        chosenSuitByNonActivePlayer = chooseCardWithKeyboard(activePlayerSuits, game.getNonActivePlayer(), game, additionalText=additionalText)
        return (chosenCardByNonActivePlayer, chosenSuitByNonActivePlayer)

    def _handleExchangeMove(self, game:Game) -> BaseResult:
        lackingSuits = self.lackingSuitsCalculator(game)
        chosenCardByNonActivePlayer, chosenSuitByNonActivePlayer  = self._opponent._nonActivePlayerChoices(lackingSuits, game)
                        
        os.system("cls")
        print(game)
        additionalText = f"{game.getActivePlayer()}, przekaż kartę {game.getNonActivePlayer()} z kształtu jaki chce otrzymać"
        print(additionalText)
        chosenCardByActivePlayer = self.showCardsAndCollectInput(game.getActivePlayer(), set(chosenSuitByNonActivePlayer), game, additionlText=additionalText)
        
        return game.tryExchangeAndPlaceCardByActivePlayer(chosenCardByActivePlayer, chosenCardByNonActivePlayer)
            
    def _handlePlaceCardMove(self, game:Game)-> BaseResult:       
        allSuits = set(e.value for e in Suit)
        card = self.showCardsAndCollectInput(game.getActivePlayer(),allSuits, game)

        return game.tryPlaceCardByActivePlayer(card)
