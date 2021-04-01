import numpy as np

import gomoku.players
from gomoku.players.player import Player


def compile_player_class(source_code, email):
    code = compile(source_code, email, 'exec', optimize=2)
    exec(code)
    if not gomoku.players.player.has_player():
        return None

    return gomoku.players.player.pop_player()

