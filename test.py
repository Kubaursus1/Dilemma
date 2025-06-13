from MoveHandlers.playerMoveHandler import PlayerMoveHandler
from MoveHandlers.human import Human
from MoveHandlers.bot import Bot
from MoveResult.errorResult import ErrorResult
from game import Game
import os
import uuid

from gameState import GameState
from utis import printWinner, is_valid_uuid


def singleGameLoop(game:Game,playersDict:dict[str,PlayerMoveHandler], gameMode: int):
    isError = None
    while(game.getGameState() == GameState.STARTED):
        os.system("cls")
        print(game)
        if isinstance(isError, ErrorResult):
            print(isError)
            isError = None
        activePlayerName = game.getActivePlayer().getName()
        result = playersDict[activePlayerName].handlePlayerMove()
        if isinstance(result, ErrorResult):
            isError = result
    playersNames = list(playersDict.keys())

    print(f"{playersNames[0]} score: {game.getPlayerByName(playersNames[0]).getScore()}")
    print(f"{playersNames[1] if gameMode == 2 else 'Bot'} score: {game.getPlayerByName(playersNames[1]).getScore()}")
    printWinner(game, gameMode)

def createGame(gameMode) -> tuple[Game, dict[str, PlayerMoveHandler]]:
    def __preparingPlayers(gameMode):
        if int(gameMode) == 1:
            firstPlayerName = input("Podaj imię gracza ")
            secondPlayerName = str(uuid.uuid4())
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

    while(firstPlayerName == secondPlayerName or len(firstPlayerName) == 0 or (len(secondPlayerName) == 0 if not is_valid_uuid(secondPlayerName) else False)):
        print()
        print("Imiona graczy muszą być różne i nie puste") if gameMode == 2 else print("Imię gracza nie może być puste")
        firstPlayerName, secondPlayerName, playerDict = __preparingPlayers(gameMode)

    game = Game(firstPlayerName, secondPlayerName)
    for player in list(playerDict.values()):
        player.setGame(game)
        
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