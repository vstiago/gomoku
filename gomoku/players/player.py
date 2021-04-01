players_list = []


class Player:
    def __init__(self, symbol, board_size):
        self._symbol = symbol
        self._size = board_size

    def first_move(self):
        pass

    def move(self, x, y):
        pass

    @staticmethod
    def register(player):
        if not issubclass(player, Player):
            print(f"Can't load player. {player.__name__} is not as sub class "
                  "of gomoku.players.Player")
            return
        try:
            p = player('O', 19)
            x, y = p.first_move()
            p.move(x, y+1)
        except Exception as e:
            print(e)
            return

        print('Registering player:', player.__name__)
        players_list.append(player)


def has_player():
    return players_list


def pop_player():
    return players_list.pop()
