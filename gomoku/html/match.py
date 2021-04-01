import dominate
from dominate.tags import *

from gomoku.models import Match


def to_html(match: Match):
    doc = dominate.document(
        title=f'{match.player_one.class_name} x {match.player_two.class_name}')
    with doc:
        li(f'{match.tournament.name} Tournament')
        li(f'Player O: {match.player_one.class_name}')
        li(f'Player X: {match.player_two.class_name}')
        li(f'Current winner: {match.current_winner}')
        br()
        li('Logs:')
        for log in match.logs:
            li(a(str(log.timestamp), href=f'match_log?id={log.id}'),
               f' winner is {log.winner}')

    return str(doc)
