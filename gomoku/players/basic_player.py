import numpy as np

from gomoku.players.player import Player


class BasicPlayer(Player):
    def __init__(self, symbol, board_size):
        super(BasicPlayer, self).__init__(symbol, board_size)

        self._opponent = 'X' if self._symbol == 'O' else 'O'
        self._board = np.full((self._size, self._size), '-')

        self._next_x = 0
        self._next_y = 0

    def first_move(self):
        x = self._next_x
        y = self._next_y
        self._board[x, y] = self._symbol
        self._next_x += 1
        self._next_y += 1

        return x, y

    def move(self, x, y):
        self._board[x, y] = self._opponent
        x = self._next_x
        y = self._next_y

        if x == self._size or y == self._size or self._board[x, y] != '-':
            x = 0
            y = 1
            while self._board[x, y] != '-':
                y += 1
                if y == self._size:
                    x += 1
                    y = 0

        self._next_x = x + 1
        self._next_y = y + 1

        self._board[x, y] = self._symbol
        return x, y


# register_player(BasicPlayer)
