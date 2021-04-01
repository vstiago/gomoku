import dominate
from dominate.tags import *

from gomoku.models import Tournament


def matches_matrix(matches):
    result = []
    player_one_id = -1
    for m in matches:
        if m.player_one_id != player_one_id:
            result.append([])
            player_one_id = m.player_one_id
        result[-1].append(m)
    return result


def to_html(t: Tournament):
    doc = dominate.document(
        title=f'{t.name} Tournament - Gomoku Bot Tournament')
    with doc:
        li(f'{t.name} Tournament')
        li(f'Board size: {t.board_size}')
        br()
        li('Score Board')
        with table():
            for score in t.scores:
                with tr():
                    td(a(score.player.class_name,
                         href=f'player?id={score.player_id}'))
                    td(score.total)
        br()
        li('Matches Board')
        matrix = matches_matrix(t.matches)
        with table():
            with tr():
                th()
                for line in matrix:
                    th(line[0].player_one.class_name[0:2])
            for line in matrix:
                with tr():
                    td(a(line[0].player_one.class_name,
                         href=f'player?id={line[0].player_one_id}'))
                    for m in line:
                        td(a(m.current_winner, href=f'match?id={m.id}'))
    return str(doc)
