#!/usr/bin/python3

import concurrent.futures

import gomoku.database
import gomoku.models
from gomoku.board import GomokuBoard, BoardStates
# import input_player
from gomoku.players import player
from gomoku.players.basic_player import BasicPlayer
from gomoku.players.random_player import RandomPlayer
from gomoku.players.reverse_player import ReversePlayer
from gomoku.score_board import ScoreBoard


class Tournament:
    def __init__(self, executor, model, timeout=0.001):
        self._executor = executor
        self._model = model
        self._board_size = model.board_size
        self._timeout = timeout

    def move(self, board, *args):
        future = self._executor.submit(*args)
        try:
            x, y = future.result(self._timeout)
            winner, status = board.play(x, y)
        except concurrent.futures.TimeoutError:
            return -1, -1, board.next, "Timeout."
        except Exception as e:
            return -1, -1, board.next, str(e)

        return x, y, winner, status

    def match(self, player1, player2):
        board = GomokuBoard(self._board_size)
        log = [f"O = {player1.__name__}", f"X = {player2.__name__}"]

        try:
            p1 = player1('O', self._board_size)
        except Exception as e:
            log.append(repr(e))
            return board.next, '\n'.join(log)

        try:
            p2 = player2('X', self._board_size)
        except Exception as e:
            log.append(repr(e))
            return board.current, '\n'.join(log)

        x, y, winner, status = self.move(board, p1.first_move)
        log.append(f"O: {x},{y}")

        while winner == BoardStates.EMPTY:
            x, y, winner, status = self.move(board, p2.move, x, y)
            log.append(f"X: {x},{y}")
            if winner != BoardStates.EMPTY:
                break

            x, y, winner, status = self.move(board, p1.move, x, y)
            log.append(f"O: {x},{y}")

        log.append(status)
        log.append(str(board))
        return winner, '\n'.join(log)


def tournament(executor, db_session, model: gomoku.models.Tournament,
               players_dict):
    print(model)
    score_board = ScoreBoard(players_dict)
    matrix_board = str()

    matches = db_session.query(gomoku.models.Match).filter(
        gomoku.models.Match.tournament_id == model.id)
    matches_dict = {}
    for match in matches:
        matches_dict[match.player_one_id, match.player_two_id] = match

    t = Tournament(executor, model)
    for idx1 in players_dict:
        p_reg1 = db_session.get(gomoku.models.Player, idx1)
        matrix_board += f'{players_dict[idx1].__name__:20}'
        for idx2 in players_dict:
            p_reg2 = db_session.get(gomoku.models.Player, idx2)
            winner, game_log = t.match(players_dict[idx1], players_dict[idx2])
            score_board.add_result(p_reg1, p_reg2, winner)
            winner = str(winner)
            matrix_board += f' {winner}'
            if (idx1, idx2) not in matches_dict:
                match = gomoku.models.Match(model, p_reg1, p_reg2, winner)
                match_log = gomoku.models.MatchLog(match, winner, game_log)
                db_session.add(match)
                db_session.add(match_log)
            else:
                match = matches_dict[idx1, idx2]
                if match.logs[-1].log != game_log:
                    match.current_winner = winner
                    match_log = gomoku.models.MatchLog(match, winner,
                                                       game_log)
                    db_session.add(match_log)

        matrix_board += '\n'

    scores = db_session.query(gomoku.models.Score).filter(
        gomoku.models.Score.tournament_id == model.id)
    scores_dict = {}
    for score in scores:
        scores_dict[score.player_id] = score

    player_id: int
    for player_id in score_board.scores:
        if player_id in scores_dict:
            scores_dict[player_id].total = score_board.scores[player_id]
        else:
            score = gomoku.models.Score(model,
                                        db_session.get(gomoku.models.Player,
                                                       player_id),
                                        score_board.scores[player_id])
            db_session.add(score)

    print('Matrix Board')
    print(matrix_board)
    model.matches_board = matrix_board

    score_board.sort()
    model.score_board = str(score_board)

    db_session.commit()


def main(argv):
    board_size = 19 if len(argv) == 1 else int(argv[1])

    players = {1: RandomPlayer, 2: ReversePlayer, 3: BasicPlayer}
    i = 4
    files = ['tv_player.py', 'fake_player.py']
    for filename in files:
        with open(filename, 'r') as file_descriptor:
            data = file_descriptor.read()
            code = compile(data, filename, 'exec', optimize=2)

            exec(code)
            if player.has_player():
                players[i] = player.pop_player()
                i += 1

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    t = gomoku.models.Tournament(board_size=board_size)
    tournament(executor, t, players)


if __name__ == "__main__":
    import sys
    main(sys.argv)
