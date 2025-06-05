import time
import colorama
import keyboard
from MoveResult.baseResult import BaseResult
from player import Player
from MoveResult.errorResult import ErrorResult
from gameState import GameState, GameResult
from rank import Rank
from suit import Suit
from card import Card
from game import Game
import os
import uuid
import random


class PlayerMoveHandler:
    def __init__(self, name):
        self._name = name
    def showCardsAndCollectInput(targetPlayer: Player, suits: set[str], additionlText=None) -> Card: 
        print(f"{targetPlayer.getName()}, wybierz kartę.")
            
        cards = list(filter(lambda card : card.getSuit().value in suits, targetPlayer.getHand()))
        print(f"[{colorama.Fore.GREEN}{cards[0]}{colorama.Style.RESET_ALL}",", " + ", ".join(str(card) for card in cards[1:]) if len(cards) != 1 else "", "]", sep="")
        return chooseCardWithKeyboard(cards, targetPlayer, additionalText=additionlText if additionlText !=None else None)
    def lackingSuitsCalculator():
            trickSuits = set(map( lambda card : card.getSuit().value, game.getTricks().getCurrentTrick().getAllCards()))
            allSuits = set(e.value for e in Suit)
            lackingSuits = allSuits-trickSuits
            return lackingSuits
    def humanChoosingSystem(self, lackingSuits):
            additionalText = f"{game.getNonActivePlayer()} przekazuje kartę {game.getActivePlayer() if isinstance(self._opponent, Human) else "Bot'owi"}\n"
            print(additionalText)
            chosenCardByNonActivePlayer = self.showCardsAndCollectInput(game.getNonActivePlayer(), lackingSuits, additionlText=additionalText)

            os.system("cls")   
            print(game)                                 
            activePlayerSuits: list[str] = list(set(map( lambda card : card.getSuit().value, game.getActivePlayer().getHand())))
            additionalText = f"{game.getNonActivePlayer()}, wybierz kolor jaki chcesz otrzymać"
            print(additionalText)
            print(f"[{colorama.Fore.GREEN}{activePlayerSuits[0]}{colorama.Style.RESET_ALL}",", " + ", ".join(str(suit) for suit in activePlayerSuits[1:]) if len(activePlayerSuits) != 1 else "", "]", sep="")
            chosenSuitByNonActivePlayer = chooseCardWithKeyboard(activePlayerSuits, game.getNonActivePlayer(), additionalText=additionalText)
            return (chosenCardByNonActivePlayer, chosenSuitByNonActivePlayer)
    def handlePlayerMove(self,game:Game)-> BaseResult:
        pass
    def setOpponent(self,opponent:"PlayerMoveHandler"):
        self._opponent = opponent
    def cardChoosingAnimation(self):
        for _ in range(4):
            for i in ["|", "/", "-", "\\"]:
                print(f"\r{i}", end="")
                time.sleep(0.15)
class Bot(PlayerMoveHandler):
    def handlePlayerMove(self, game:Game):
        def handlePlaceCardMove() -> BaseResult:
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
            self.cardChoosingAnimation()
            return game.tryPlaceCardByActivePlayer(chossenCard)
        def handleExchangeMove() -> BaseResult:
            lackingSuits = self.lackingSuitsCalculator()
            chosenCardByNonActivePlayer, chosenSuitByNonActivePlayer = self.humanChoosingSystem(lackingSuits)
            os.system("cls")
            print(game)
            print("Bot wybiera kartę")
            self.cardChoosingAnimation()
            chosenCardByActivePlayer = random.choice(list(filter(lambda card : card.getSuit().value in set(chosenSuitByNonActivePlayer), game.getActivePlayer().getHand())))
            return game.tryExchangeAndPlaceCardByActivePlayer(chosenCardByActivePlayer, chosenCardByNonActivePlayer)
        return handleExchangeMove() if game.getActivePlayerCanNotPlaceCard() else handlePlaceCardMove()
           
class Human(PlayerMoveHandler):
    def handlePlayerMove(self,game:Game)-> BaseResult:
        def handleExchangeMove() -> BaseResult:
            lackingSuits = self.lackingSuitsCalculator()

            if isinstance(self._opponent, Human):
                chosenCardByNonActivePlayer, chosenSuitByNonActivePlayer = self.humanChoosingSystem(lackingSuits)
            elif isinstance(self._opponent, Bot):
                print("Bot wybiera kartę")
                self.cardChoosingAnimation()
                chosenCardByNonActivePlayer = random.choice(list(filter(lambda card : card.getSuit().value in lackingSuits, game.getNonActivePlayer().getHand())))
                os.system("cls")
                print(game)
                print("Bot wybiera kształt")
                self.cardChoosingAnimation()
                chosenSuitByNonActivePlayer = list(set(map(lambda card : card.getSuit().value, game.getActivePlayer().getHand())))
            os.system("cls")
            print(game)
            additionalText = f"{game.getActivePlayer()}, przekaż kartę {game.getNonActivePlayer()} z kształtu jaki chce otrzymać"
            print(additionalText)
            chosenCardByActivePlayer = self.showCardsAndCollectInput(game.getActivePlayer(), set(chosenSuitByNonActivePlayer), additionlText=additionalText)
            
            return game.tryExchangeAndPlaceCardByActivePlayer(chosenCardByActivePlayer, chosenCardByNonActivePlayer)

        def handlePlaceCardMove()-> BaseResult:       
            allSuits = set(e.value for e in Suit)
            card = self.showCardsAndCollectInput(game.getActivePlayer(),allSuits)

            return game.tryPlaceCardByActivePlayer(card)
    
        return handleExchangeMove() if game.getActivePlayerCanNotPlaceCard() else handlePlaceCardMove()

def printWinner(game: Game, gameMode: int):
    result = ""
    match game.getGameResult():
        case GameResult.WINNER_FIRST:
            result = f"{game.getFirstPlyerName()} is the winner of the game"
        case GameResult.WINNER_SECOND:
            if gameMode == 2:
                result = f"{game.getSecondPlayerName()} is the winner of the game"
            else:
                result = "You lose"
        case GameResult.DRAW:
            result = "No one wins. Draw"
    print(result)

def chooseCardWithKeyboard(hand: list[Card] | list[str], targetPlayer: Player, additionalText=None) -> Card:
    i = 0
    chosenCard = None
    def refreshTerminal():
        os.system("cls")
        print(game)
        print(additionalText) if additionalText != None else None
        print(f"{targetPlayer.getName()}, wybierz kartę.") if isinstance(hand[0], Card) else None
        print(f"[", ', '.join(f"{colorama.Fore.GREEN}{card}{colorama.Style.RESET_ALL}" if idx == i else str(card) for idx, card in enumerate(hand)), "]", sep="")
    def changeIdxToPrevious():
        nonlocal i
        i = (i - 1) % len(hand)
        refreshTerminal()
    def changeIdxToNext():
        nonlocal i
        i = (i + 1) % len(hand)
        refreshTerminal()

    def chooseThisCard():
        nonlocal chosenCard
        chosenCard = hand[i]
        keyboard.unhook_all()
    
    keyboard.add_hotkey('left', changeIdxToPrevious)
    keyboard.add_hotkey('right', changeIdxToNext)
    keyboard.add_hotkey('enter', chooseThisCard)

    while chosenCard is None:
        time.sleep(0.05)

    return chosenCard

def singleGameLoop(game:Game,playersDict:dict[str,PlayerMoveHandler], gameMode: int):
    isError = None
    while(game.getGameState() == GameState.STARTED):
        os.system("cls")
        print(game)
        if isinstance(isError, ErrorResult):
            print(isError)
            isError = None
        activePlayerName = game.getActivePlayer().getName()
        result = playersDict[activePlayerName].handlePlayerMove(game)
        if isinstance(result, ErrorResult):
            isError = result
    playersNames = list(playersDict.keys())

    print(f"{playersNames[0]} score: {game.getPlayerByName(playersNames[0]).getScore()}")
    print(f"{playersNames[1] if gameMode == 2 else "Bot"} score: {game.getPlayerByName(playersNames[1]).getScore()}")
    printWinner(game, gameMode)

def createGame(gameMode) -> tuple[Game, dict[str, PlayerMoveHandler]]:
    def __preparingPlayers(gameMode):
        if int(gameMode) == 1:
            firstPlayerName = input("Podaj imię gracza ")
            secondPlayerName = uuid.uuid4()
            human = Human(firstPlayerName)
            bot = Bot(secondPlayerName)
            human.setOpponent(bot)
            bot.setOpponent(human)
            playerDict = {firstPlayerName: human, secondPlayerName: bot}
        else:
            firstPlayerName = input("Podaj imię pierwszego gracza ")
            secondPlayerName = input("Podaj imię drugiego gracza ")
            human1 = Human(firstPlayerName)
            human2 = Human(secondPlayerName)
            human1.setOpponent(human2)
            human2.setOpponent(human1)
            playerDict = {firstPlayerName: human1, secondPlayerName: human2}
        return firstPlayerName,secondPlayerName,playerDict
    firstPlayerName, secondPlayerName, playerDict = __preparingPlayers(gameMode)

    while(firstPlayerName == secondPlayerName or len(firstPlayerName) == 0 or len(secondPlayerName) == 0):
        print()
        print("Imiona graczy muszą być różne i nie puste") if gameMode == 2 else print("Imię gracza nie może być puste")
        firstPlayerName, secondPlayerName, playerDict = __preparingPlayers(gameMode)

    game = Game(firstPlayerName, secondPlayerName)
        
    return (game, playerDict)

gameMode = input("Wybierz tryb gry: 1- gra z Botem, 2- gra w dwie osoby: ")
while(gameMode not in ["1", "2"]):
    print("Nie ma takiego trybu gry wpisz odpowiednie numery ")
    gameMode = input("1- gra z botem, 2- gra w dwie osoby ")
while(True):
    game, playersDict = createGame(gameMode)
    game.startNewDealAndStartGame()
    
    singleGameLoop(game,playersDict, gameMode)

    shouldPlayAgain = input("Czy chasz zagrać ponownie.(Y/N) ")
    if shouldPlayAgain.upper() == "N":
        break
    gameMode = input("Wybierz '1' Jeżeli chcesz jeszcze raz zagrać z Botem lub '2' jeżeli z drugim graczem: ")
# TODO: oddzielić classy MoveHandlers do innego pliku
# TODO: refactoring