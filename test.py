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
        self.__name = name
    def handlePlayerMove(self,game:Game)-> BaseResult:
        pass
    def setOpponent(self,opponent:"PlayerMoveHandler"):
        self.__opponent = opponent
class Bot(PlayerMoveHandler):
   def handlePlayerMove(self, game:Game):
       def handlePlaceCardMove() -> BaseResult:
            if game.getTricks().getCurrentTrick().len() == 1:
                pass
            elif game.getTricks().getCurrentTrick().len() == 3:
                pass
            else:
                actualPlayerHand = game.getPlayerByName(self.__name).getHand()
                trickSuits = set(map( lambda card : card.getSuit().value, game.getTricks().getCurrentTrick().getAllCards()))
                allSuits = set(e.value for e in Suit)
                lackingSuits = allSuits-trickSuits
                cards = list(filter(lambda card : card.getSuit().value in lackingSuits, actualPlayerHand))
                chossenCard = random.choice(cards)
            game.tryPlaceCardByActivePlayer(chossenCard)
           
class Human(PlayerMoveHandler):
    def handlePlayerMove(self,game:Game)-> BaseResult:
        def showCardsAndCollectInput(targetPlayer: Player, suits: set[str]) -> Card: 
            print(f"{targetPlayer.getName()}, wybierz kartę.")
            
            cards = list(filter(lambda card : card.getSuit().value in suits, targetPlayer.getHand()))
            print(f"[{colorama.Fore.GREEN}{cards[0]}{colorama.Style.RESET_ALL}", *cards[1:-1], sep=", ", end=f", {cards[-1]}]\n")
            return chooseCardWithKeyboard(cards, targetPlayer)
        def handleExchangeMove() -> BaseResult:
            trickSuits = set(map( lambda card : card.getSuit().value, game.getTricks().getCurrentTrick().getAllCards()))
            allSuits = set(e.value for e in Suit)
            lackingSuits = allSuits-trickSuits
        
            #przeciwnik -oddzielna funkcja w klasie PlayerMoveHandler
            print(f"{game.getNonActivePlayer()} przekazuje kartę {game.getActivePlayer()}\n")
            chosenCardByNonActivePlayer = showCardsAndCollectInput(game.getNonActivePlayer(), lackingSuits)

            #przeciwnik -oddzielna funkcja w klasie PlayerMoveHandler                                                          
            activePlayerSuits = list(set(map( lambda card : card.getSuit().value, game.getActivePlayer().getHand())))
            print(f"{game.getNonActivePlayer()}, wybierz kolor jaki chcesz otrzymać")
            print(activePlayerSuits)
            chosenSuitByNonActivePlayer = activePlayerSuits[int(input("nr: "))]
            
            #my
            chosenCardByActivePlayer = showCardsAndCollectInput(game.getActivePlayer(), set(chosenSuitByNonActivePlayer))
            
            return game.tryExchangeAndPlaceCardByActivePlayer(chosenCardByActivePlayer, chosenCardByNonActivePlayer)
        def handlePlaceCardMove()-> BaseResult:       
            allSuits = set(e.value for e in Suit)
            card = showCardsAndCollectInput(game.getActivePlayer(),allSuits)

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

def chooseCardWithKeyboard(hand: list[Card], targetPlayer: Player) -> Card:
    i = 0
    chosenCard = None
    def refreshTerminal():
        os.system("cls")
        print(game)
        print(f"{targetPlayer.getName()}, wybierz kartę.")
        cards = ', '.join(f"{colorama.Fore.GREEN}{card}{colorama.Style.RESET_ALL}" if idx == i else str(card) for idx, card in enumerate(hand))
        print(f"[{cards}]")
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
    
    for p in game.getPlayers():
        print(f"{p.getName()} score: {p.getScore()}")
    printWinner(game, gameMode)

def createGame(gameMode) -> tuple[Game, dict[str, PlayerMoveHandler]]:
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

    game = Game(firstPlayerName, secondPlayerName)
        
    return (game, playerDict)

while(True):
    gameMode = input("Wybierz tryb gry: 1- gra z Botem, 2- Gra z człowiekiem")
    game, playersDict = createGame(gameMode)
    game.startNewDealAndStartGame()
    
    singleGameLoop(game,playersDict, gameMode)

    shouldPlayAgain = input("Czy chasz zagrać ponownie.(Y/N) ")
    if shouldPlayAgain.upper() == "N":
        break
# TODO: dokończyć przypadki bota na ruchu w tricku
# TODO: załatwić handleExchengeMove