import os
import random
from MoveHandlers.playerMoveHandler import PlayerMoveHandler
from MoveResult.baseResult import BaseResult
from card import Card
import game
from suit import Suit

class Bot(PlayerMoveHandler):

    def _nonActivePlayerChoices(self,lackingSuits) -> tuple[Card, Suit]:
        print("Bot wybiera kartę")
        self.cardChoosingAnimation(6)
        chosenCardByNonActivePlayer = random.choice(list(filter(lambda card : card.getSuit().value in lackingSuits, game.getNonActivePlayer().getHand())))
        os.system("cls")
        print(game)
        print("Bot wybiera kształt")
        self.cardChoosingAnimation(6)
        chosenSuitByNonActivePlayer = list(set(map(lambda card : card.getSuit().value, game.getActivePlayer().getHand())))
        return (chosenCardByNonActivePlayer, chosenSuitByNonActivePlayer)
        
    def _handlePlaceCardMove(self) -> BaseResult:
        trickSuits = set(map( lambda card : card.getSuit().value, game.getTricks().getCurrentTrick().getAllCards()))
        allSuits = set(e.value for e in Suit)
        lackingSuits = allSuits-trickSuits
        cards = list(filter(lambda card : card.getSuit().value in lackingSuits, game.getPlayerByName(self._name).getHand())) if lackingSuits else game.getPlayerByName(self._name).getHand()
        currentTrick = game.getTricks().getCurrentTrick()
        if currentTrick.len() == 1:
            firstCardRank = currentTrick.first().getRank().value
            bestCardRankChoose = list(filter(lambda card : card.getRank().value > firstCardRank and card.getRank().value <= firstCardRank+3, cards))
            if bestCardRankChoose:
                chossenCard = random.choice(bestCardRankChoose)
            else:
                chossenCard = random.choice(cards)
        elif game.getTricks().getCurrentTrick().len() == 3:
            botCradRank = currentTrick.first().getRank().value
            playerCardsRank = sum(map(lambda card : card.getRank().value ,currentTrick.getCardsByIndexes([1,2])))
            botHighestCardRank = max(map(lambda card : card.getRank().value, cards))
            if (botCradRank + botHighestCardRank) > playerCardsRank:
                chossenCard = list(filter(lambda card : card.getRank().value == botHighestCardRank, cards))[0]
            else:
                chossenCard = random.choice(cards)
        else:
            chossenCard = random.choice(cards)
        self.cardChoosingAnimation(4)
        return game.tryPlaceCardByActivePlayer(chossenCard)
        
    def _handleExchangeMove(self) -> BaseResult:
        lackingSuits = self.lackingSuitsCalculator()        
        chosenCardByNonActivePlayer, chosenSuitByNonActivePlayer  = self._opponent._nonActivePlayerChoices(lackingSuits)
        
        os.system("cls")
        print(game)
        print("Bot wybiera kartę")
        self.cardChoosingAnimation(6)
        chosenCardByActivePlayer = random.choice(list(filter(lambda card : card.getSuit().value in set(chosenSuitByNonActivePlayer), game.getActivePlayer().getHand())))
        return game.tryExchangeAndPlaceCardByActivePlayer(chosenCardByActivePlayer, chosenCardByNonActivePlayer)
           