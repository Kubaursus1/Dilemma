import os
import random
from MoveHandlers.playerMoveHandler import PlayerMoveHandler
from MoveResult.baseResult import BaseResult
from card import Card
from suit import Suit

class Bot(PlayerMoveHandler):

    def _nonActivePlayerChoices(self,lackingSuits) -> tuple[Card, Suit]:
        print("Bot wybiera kartę")
        self.cardChoosingAnimation(6)
        chosenCardByNonActivePlayer = random.choice(list(filter(lambda card : card.getSuit().value in lackingSuits, self._game.getNonActivePlayer().getHand())))
        os.system("cls")
        print(self._game)
        print("Bot wybiera kształt")
        self.cardChoosingAnimation(6)
        chosenSuitByNonActivePlayer = list(set(map(lambda card : card.getSuit().value, self._game.getActivePlayer().getHand())))
        return (chosenCardByNonActivePlayer, chosenSuitByNonActivePlayer)
        
    def _handlePlaceCardMove(self) -> BaseResult:
        trickSuits = set(map( lambda card : card.getSuit().value, self._game.getTricks().getCurrentTrick().getAllCards()))
        allSuits = set(e.value for e in Suit)
        lackingSuits = allSuits-trickSuits
        cards = list(filter(lambda card : card.getSuit().value in lackingSuits, self._game.getPlayerByName(self._name).getHand())) if lackingSuits else self._game.getPlayerByName(self._name).getHand()
        currentTrick = self._game.getTricks().getCurrentTrick()
        if currentTrick.len() == 1:
            firstCardRank = currentTrick.first().getRank().value
            bestCardRankChoose = list(filter(lambda card : card.getRank().value > firstCardRank and card.getRank().value <= firstCardRank+2, cards))
            if bestCardRankChoose:
                chossenCard = random.choice(bestCardRankChoose)
            else:
                chossenCard = random.choice(cards)
        elif self._game.getTricks().getCurrentTrick().len() == 3:
            botCradRank = currentTrick.first().getRank().value
            playerCardsRank = sum(map(lambda card : card.getRank().value ,currentTrick.getCardsByIndexes([1,2])))
            botHighestCardRank = max(map(lambda card : card.getRank().value, cards))
            if (botCradRank + botHighestCardRank) > playerCardsRank:
                chossenCard = list(filter(lambda card : card.getRank().value == botHighestCardRank, cards))[0]
            else:
                chossenCard = list(filter(lambda card : card.getRank().value == min(map(lambda card : card.getRank().value, cards)),cards))[0]
        else:
            chossenCard = random.choice(cards)
        self.cardChoosingAnimation(4)
        return self._game.tryPlaceCardByActivePlayer(chossenCard)
        
    def _handleExchangeMove(self) -> BaseResult:
        lackingSuits = self.lackingSuitsCalculator(self._game)        
        chosenCardByNonActivePlayer, chosenSuitByNonActivePlayer  = self._opponent._nonActivePlayerChoices(lackingSuits, self._game)
        
        os.system("cls")
        print(self._game)
        print("Bot wybiera kartę")
        self.cardChoosingAnimation(6)
        chosenCardByActivePlayer = random.choice(list(filter(lambda card : card.getSuit().value in set(chosenSuitByNonActivePlayer), self._game.getActivePlayer().getHand())))
        return self._game.tryExchangeAndPlaceCardByActivePlayer(chosenCardByActivePlayer, chosenCardByNonActivePlayer)
           