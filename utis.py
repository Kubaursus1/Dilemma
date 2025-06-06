import os
import time
import colorama
import keyboard
from card import Card
from game import Game
import game
from gameState import GameResult
from player import Player


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
