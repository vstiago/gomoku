from gomoku.board import BoardStates


class ScoreBoard:
    def __init__(self, players):
        self._players = players
        self._scores= {}
        for idx in players:
            self._scores[idx] = 0

        self._sorted_score = []

    @property
    def scores(self):
        return self._scores

    def add_result(self, p1, p2, winner):
        if winner == BoardStates.PLAYER_ONE:
            self._scores[p1.id] += 3
        elif winner == BoardStates.PLAYER_TWO:
            self._scores[p2.id] += 3
        else:
            self._scores[p1.id] += 1
            self._scores[p2.id] += 1

    def sort(self):
        self._sorted_score = []
        for idx in self._scores:
            self._sorted_score.append(
                (self._players[idx].__name__, self._scores[idx]))

        self._sorted_score.sort(key=lambda x: x[1], reverse=True)

    def __str__(self):
        buf = str()
        for name, score in self._sorted_score:
            buf += f'{name:20}:{score:3}\n'
        return buf
