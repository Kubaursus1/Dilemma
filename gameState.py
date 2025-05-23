from enum import Enum


class GameState(Enum):
    NOT_STARTED = 0
    STARTED = 1
    ENDED = 2
    
    
class GameResult(Enum):
    WINNER_FIRST = 0
    WINNER_SECOND = 1
    DRAW = 2
    