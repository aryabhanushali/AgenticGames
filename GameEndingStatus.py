from enum import Enum


class Status(Enum):
    """
    Represents the states a game could finish in.
    """
    PLAYER_1_WINS = 'Player 1 Wins'
    PLAYER_1_INVALID_MOVE = 'Player 1 Invalid Move'

    PLAYER_2_WINS = 'Player 2 Wins'
    PLAYER_2_INVALID_MOVE = 'Player 2 Invalid Move'

    PLAYER_3_WINS = 'Player 3 Wins'
    PLAYER_3_INVALID_MOVE = 'Player 3 Invalid Move'

    TIE = 'Tie'
