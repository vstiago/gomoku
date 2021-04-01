from gomoku.players.player import Player


class ReversePlayer(Player):
    def first_move(self):
        return int(self._size / 2), int(self._size / 2)

    def move(self, x, y):
        return y, x


# register_player(ReversePlayer)
