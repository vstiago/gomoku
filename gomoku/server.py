import concurrent.futures
# import os

from flask import Flask
from flask import request, render_template, make_response

import gomoku.models
import gomoku.players.player
import gomoku.tournament
import gomoku.html.player
import gomoku.html.tournament
import gomoku.html.match
from gomoku.database import db_session
from gomoku.players.basic_player import BasicPlayer
from gomoku.players.random_player import RandomPlayer
from gomoku.players.reverse_player import ReversePlayer
from gomoku.compile_player import compile_player_class

player_classes = [RandomPlayer, ReversePlayer, BasicPlayer]


def create_db():
    gomoku.database.init_db()
    session = gomoku.database.db_session()
    if not session.query(gomoku.models.Tournament).all():
        for name, board_size in [('Tiny', 5), ('Small', 9), ('Medium', 13),
                                 ('Large', 19), ('Huge', 26)]:
            t = gomoku.models.Tournament(name, board_size)
            print('add', t)
            session.add(t)
        session.commit()

    model_players = session.query(gomoku.models.Player).all()
    if not model_players:
        session.add_all(
            [gomoku.models.Player("random", "r@nd.om", "<static code>",
                                  'RandomPlayer'),
             gomoku.models.Player("reverse", "esrever@msn.com",
                                  "<static code>", 'ReversePlayer'),
             gomoku.models.Player("basic", "basic@gmail.com",
                                  "<static code>", 'BasicPlayer')])
        status = session.commit()
        print('commit status', status)
        model_players = session.query(gomoku.models.Player).all()

    for p in model_players[3:]:
        player_class = compile_player_class(p.code, p.email)
        if player_class is None:
            print('Failed to load code.')
            del p
        player_classes.append(player_class)

    p_dict = {}
    for model, code in zip(model_players, player_classes):
        p_dict[model.id] = code

    print('players_dict', p_dict)
    return p_dict


app = Flask(__name__, instance_relative_config=True)
players_dict = create_db()

# ensure the instance folder exists
# try:
#     os.makedirs(app.instance_path)
# except OSError:
#     pass


@app.route('/')
def index():
    session = gomoku.database.db_session
    tournaments = session.query(gomoku.models.Tournament).all()
    print(len(tournaments))
    return render_template("home.html", tournaments=tournaments)


@app.route('/tournament', methods=['GET'])
def tournament():
    session = gomoku.database.db_session()
    t_id = int(request.args.get('id'))
    t = session.get(gomoku.models.Tournament, t_id)
    return gomoku.html.tournament.to_html(t)


@app.route('/player', methods=['GET'])
def player():
    session = gomoku.database.db_session()
    p_id = int(request.args.get('id'))
    p = session.get(gomoku.models.Player, p_id)
    return gomoku.html.player.to_html(p)


@app.route('/match', methods=['GET'])
def match():
    session = gomoku.database.db_session()
    m_id = int(request.args.get('id'))
    m = session.get(gomoku.models.Match, m_id)
    return gomoku.html.match.to_html(m)


@app.route('/match_log', methods=['GET'])
def match_log():
    session = gomoku.database.db_session()
    m_id = int(request.args.get('id'))
    m = session.get(gomoku.models.MatchLog, m_id)

    response = make_response(m.log)
    response.headers['Content-Type'] = 'text/plain'
    return response


@app.route('/submit')
def submit_form():
    return render_template('submit-form.html')


@app.route('/submit', methods=['POST'])
def my_form_post():
    name = request.form['name']
    email = request.form['email']
    source_code = request.form['source_code']
    session = gomoku.database.db_session()

    p = session.query(gomoku.models.Player).filter(
        gomoku.models.Player.email == email).first()
    if p is None:
        p = gomoku.models.Player(name, email, source_code)
        session.add(p)

    p_class = compile_player_class(p.code, p.email)
    if p_class is None:
        session.rollback()
        return f'Failed to compile code for {email}.'

    p.class_name = p_class.__name__
    session.commit()

    players_dict[p.id] = p_class

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    for t in session.query(gomoku.models.Tournament):
        gomoku.tournament.tournament(executor, session, t, players_dict)
    return name + " done."


@app.teardown_appcontext
def shutdown_session(exception=None):
    print(exception)
    db_session.remove()
