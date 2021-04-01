import random
import numpy as np
from gomoku.players.player import Player


class RandomPlayer(Player):
    def __init__(self, symbol, board_size):
        super(RandomPlayer, self).__init__(symbol, board_size)

        self._opponent = 'X' if self._symbol == 'O' else 'O'
        self._board = np.full((self._size, self._size), '-')

    def first_move(self):
        x = random.randint(0, self._size - 1)
        y = random.randint(0, self._size - 1)

        self._board[x, y] = self._symbol

        return x, y

    def move(self, x, y):
        self._board[x, y] = self._opponent

        while self._board[x, y] != '-':
            x = random.randint(0, self._size - 1)
            y = random.randint(0, self._size - 1)

        self._board[x, y] = self._symbol

        return x, y

