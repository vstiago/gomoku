import enum
import numpy as np


class BoardStates(enum.Enum):
    EMPTY = 0
    PLAYER_ONE = 1
    PLAYER_TWO = 2
    DRAW = 3
    BORDER = 4

    def __str__(self):
        if self == BoardStates.EMPTY:
            return '-'
        elif self == BoardStates.PLAYER_ONE:
            return 'O'
        elif self == BoardStates.PLAYER_TWO:
            return 'X'
        elif self == BoardStates.DRAW:
            return '='
        elif self == BoardStates.BORDER:
            return '#'
        return '!'

    def __repr__(self):
        return self.__str__()


def count_five(turn, min_i, max_i, board_slice):
    count = 0
    for i in range(min_i, max_i):
        if board_slice(i) == turn:
            count += 1
            if count == 5:
                return True
        else:
            count = 0
    return False


def board_slices(board, x, y):
    size = len(board)

    min_x = max(-x, - 4)
    max_x = min(5, size - x)
    yield min_x, max_x, lambda i: board[x + i, y]

    min_y = max(-y, -4)
    max_y = min(5, size - y)
    yield min_y, max_y, lambda i: board[x, y + i]

    min_xy = max(min_x, min_y)
    max_xy = min(max_x, max_y)
    yield min_xy, max_xy, lambda i: board[x + i, y + i]

    min_yx = max(min_x, -max_y + 1)
    max_yx = min(max_x, -min_y + 1)
    yield min_yx, max_yx, lambda i: board[x + i, y - i]

    return


class GomokuBoard:
    def __init__(self, board_size):
        self._size = board_size
        self._moves = 0
        self._total_moves = board_size * board_size

        self._board = np.full((self._size, self._size), BoardStates.EMPTY)

        self._current = BoardStates.PLAYER_ONE
        self._next = BoardStates.PLAYER_TWO
        numbers = []
        for i in range(self._size):
            numbers.append(f'{i:2}')
        self._header = '  {}'.format(''.join(numbers))

    @property
    def current(self):
        return self._current

    @property
    def next(self):
        return self._next

    def win(self, x, y):
        for min_i, max_i, board_slice in board_slices(self._board, x, y):
            if count_five(self.current, min_i, max_i, board_slice):
                return True
        return False

    def play(self, x, y):
        if x < 0 or x >= self._size or y < 0 or y >= self._size:
            return self._next, "Invalid movement."

        if self._board[x, y] != BoardStates.EMPTY:
            return self._next, "Position occupied."

        self._board[x, y] = self.current
        if self.win(x, y):
            return self.current, f"Winner is {self.current}"

        self._moves += 1
        if self._moves >= self._total_moves:
            return BoardStates.DRAW, "Draw. Table is full."

        self._current, self._next = self._next, self._current
        return BoardStates.EMPTY, ""

    def __str__(self):
        buf = [self._header]
        for idx, line in enumerate(self._board):
            line_str = str(line)
            buf.append(f'{idx:2} {line_str[1:-1]}')

        return '\n'.join(buf)
