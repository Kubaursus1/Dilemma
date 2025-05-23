import time
import colorama
import keyboard
from player import Player
from MoveResult.errorResult import ErrorResult
from gameState import GameState, GameResult
from rank import Rank
from suit import Suit
from card import Card
from game import Game
import os


firstPlayerName = input("Podaj imię pierwszego gracza ")
secondPlayerName = input("Podaj imię drugiego gracza ")


game = Game(firstPlayerName, secondPlayerName)

def printWinner(gameResult):
    result = ""
    match gameResult:
        case GameResult.WINNER_FIRST:
            result = f"{firstPlayerName} is the winner of the game"
        case GameResult.WINNER_SECOND:
            result = f"{secondPlayerName} is the winner of the game"
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
        cards = ', '.join(
        f"{colorama.Fore.GREEN}{card}{colorama.Style.RESET_ALL}" if idx == i else str(card)
        for idx, card in enumerate(hand))
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

def singleGameLoop(game:Game):
    isError = None
    while(game.getGameState() == GameState.STARTED):
        os.system("cls")
        print(game)
        if isinstance(isError, ErrorResult):
            print(isError)
            isError = None
        result = handlePlayerMove(game)
        if isinstance(result, ErrorResult):
            isError = result
    
    for p in game.getPlayers():
        print(f"{p.getName()} score: {p.getScore()}")
    printWinner(game.getGameResult())

def handlePlayerMove(game:Game):
    def showCardsAndCollectInput(targetPlayer: Player, suits: set[str]) -> Card: 
        print(f"{targetPlayer.getName()}, wybierz kartę.")
        
        cards = list(filter(lambda card : card.getSuit().value in suits, targetPlayer.getHand()))
        print(f"[{colorama.Fore.GREEN}{cards[0]}{colorama.Style.RESET_ALL}", *cards[1:-1], sep=", ", end=f", {cards[-1]}]\n")
        return chooseCardWithKeyboard(cards, targetPlayer)
    def handleExchangeMove():      
        trickSuits = set(map( lambda card : card.getSuit().value, game.getTricks().getCurrentTrick().getAllCards()))
        allSuits = set(e.value for e in Suit)
        lackingSuits = allSuits-trickSuits
     
        print(f"{game.getNonActivePlayer()} przekazuje kartę {game.getActivePlayer()}\n")
        chosenCardByNonActivePlayer = showCardsAndCollectInput(game.getNonActivePlayer(), lackingSuits)
                                                        
        activePlayerSuits = list(set(map( lambda card : card.getSuit().value, game.getActivePlayer().getHand())))
        print(f"{game.getNonActivePlayer()}, wybierz kolor jaki chcesz otrzymać")
        print(activePlayerSuits)
        chosenSuitByNonActivePlayer = activePlayerSuits[int(input("nr: "))]
        
        chosenCardByActivePlayer = showCardsAndCollectInput(game.getActivePlayer(), set(chosenSuitByNonActivePlayer))
        
        return game.tryExchangeAndPlaceCardByActivePlayer(chosenCardByActivePlayer, chosenCardByNonActivePlayer)
    def handlePlaceCardMove():        
        allSuits = set(e.value for e in Suit)
        card = showCardsAndCollectInput(game.getActivePlayer(),allSuits)

        return game.tryPlaceCardByActivePlayer(card)
    
    return handleExchangeMove() if game.getActivePlayerCanNotPlaceCard() else handlePlaceCardMove()

while(True):
    game.startNewDealAndStartGame()
    
    singleGameLoop(game)

    shouldPlayAgain = input("Czy chasz zagrać ponownie.(Y/N) ")
    if shouldPlayAgain.upper() == "N":
        break
