import dominate
from dominate.tags import *
from gomoku.models import Player


def to_html(player: Player):
    doc = dominate.document(
        title=f'{player.class_name} - Gomoku Bot Tournament')
    with doc:
        li(player.class_name)
        li(f'Author: {player.name}')
        br()
        with table():
            with tr():
                th('Tournament')
                th('Score')
            for score in player.scores:
                with tr():
                    td(score.tournament.name)
                    td(score.total)
        br()
        with table():
            with tr():
                th('Tournament')
                th('Player O')
                th('Player X')
                th('Winner')

            all_matches = player.o_matches + player.x_matches
            for match in all_matches:
                with tr():
                    td(match.tournament.name)
                    td(match.player_one.class_name)
                    td(match.player_two.class_name)
                    td(match.current_winner)
                    td(a('details', href=f'match?id={match.id}'))

    return str(doc)
