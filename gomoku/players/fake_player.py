import numpy as np

from gomoku.players.player import Player


class FakePlayer(Player):
    def __init__(self, symbol, board_size):
        Player.__init__(self, symbol, board_size)
        self._symbol = symbol
        self._size = board_size
        self.EMPTY = 0
        self.MINE = 1
        self.OPPONENT = 2
        self.BORDER = 3

        self._board = np.full((self._size, self._size), self.EMPTY)
        self._scores = np.full((self._size, self._size, 4), 1.0)

        self._x = 0
        self._y = 0

    def first_move(self):
        x = y = int(self._size / 2)
        self._board[x, y] = self.MINE
        self.update_scores(x, y)
        return x, y

    def move(self, x, y):
        self._board[x, y] = self.OPPONENT
        self.update_scores(x, y)

        max_scores = -1.0
        for i in range(0, self._size):
            for j in range(0, self._size):
                total_scores = sum(self._scores[i, j])
                if total_scores > max_scores:
                    max_scores = total_scores
                    x = i
                    y = j

        self._board[x, y] = self.MINE
        self.update_scores(x, y)
        return x, y

    def new_score_me(self, board_slice, shift, me):
        if board_slice(shift) != self.EMPTY:
            return -1.0

        total_free = 1
        adjacent = 0
        counter = 0
        i = 1
        right_free = False

        piece = board_slice(shift + i)
        while piece == me or piece == self.EMPTY:
            if piece == me:
                counter += 1
                if adjacent + 1 == i:
                    adjacent += 1
            else:
                right_free = True
            i += 1
            piece = board_slice(shift + i)

        total_free += i - 1
        total_adjacent = adjacent
        adjacent = 0
        left_free = False
        i = 1
        piece = board_slice(shift - i)
        while piece == me or piece == self.EMPTY:
            if piece == me:
                counter += 1
                if adjacent + 1 == i:
                    adjacent += 1
            else:
                left_free = True
            i += 1
            piece = board_slice(shift - i)

        total_adjacent += adjacent
        total_free += i - 1

        if total_free < 5:
            return 0.0

        if total_adjacent == 4:
            return 10000000.0

        if total_adjacent == 3:
            if left_free and right_free:
                return 1000000.0
            return 1000.0

        if total_adjacent == 2:
            if left_free and right_free:
                return 400.0

        return 100.0 * total_adjacent + 10.0 * counter + total_free

    def new_score(self, board_slice, shift):
        attack_score = self.new_score_me(board_slice, shift, self.MINE)
        defense_score = self.new_score_me(board_slice, shift, self.OPPONENT)
        return 1.1 * attack_score + defense_score

    def output(self, x_i, y_i):
        if 0 <= x_i < self._size and 0 <= y_i < self._size:
            return self._board[x_i, y_i]
        else:
            return '#'

    def x_slice(self, idx):
        x_i = self._x + idx
        return self.output(x_i, self._y)

    def y_slice(self, idx):
        y_i = self._y + idx
        return self.output(self._x, y_i)

    def xy_slice(self, idx):
        x_i = self._x + idx
        y_i = self._y + idx
        return self.output(x_i, y_i)

    def yx_slice(self, idx):
        x_i = self._x + idx
        y_i = self._y - idx
        return self.output(x_i, y_i)

    def board_slices(self, x, y):
        self._x = x
        self._y = y

        return [self.x_slice, self.y_slice, self.xy_slice, self.yx_slice]

    def update_scores(self, x, y):
        slices = self.board_slices(x, y)

        bla = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for idx, slice_ref in enumerate(slices):
            for i in range(-4, 5):
                if slice_ref(i) == '#':
                    continue

                dx, dy = bla[idx]
                x_i = x + dx * i
                y_i = y + dy * i
                self._scores[x_i, y_i, idx] = self.new_score(slice_ref, i)


Player.register(FakePlayer)
