from sqlalchemy import Column, Integer, String, Text, ForeignKey, \
    UniqueConstraint, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from gomoku.database import Base


class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), unique=True)
    email = Column(String(200), unique=True)
    code = Column(Text)
    class_name = Column(String(200))
    o_matches = relationship('Match', foreign_keys="[Match.player_one_id]",
                             back_populates='player_one')
    x_matches = relationship('Match', foreign_keys="[Match.player_two_id]",
                             back_populates='player_two')
    scores = relationship('Score', back_populates='player',
                          order_by='Score.tournament_id')

    def __init__(self, name=None, email=None, code=None, class_name=None):
        self.name = name
        self.email = email
        self.code = code
        self.class_name = class_name

    def __repr__(self):
        return f'Player {self.id} name={self.name} email={self.email}'


class Tournament(Base):
    __tablename__ = 'tournaments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), unique=True)
    board_size = Column(Integer, unique=True)
    score_board = Column(Text)
    matches_board = Column(Text)

    scores = relationship('Score', back_populates='tournament',
                          order_by='desc(Score.total)')
    matches = relationship('Match', back_populates='tournament',
                           order_by='and_(Match.player_one_id, Match.player_two_id)')

    def __init__(self, name=None, board_size=None, score_board=None,
                 matches_board=None):
        self.name = name
        self.board_size = board_size
        self.score_board = score_board
        self.matches_board = matches_board

    def __repr__(self):
        return f'<Tournament {self.id}>'


class Score(Base):
    __tablename__ = 'scores'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tournament_id = Column(Integer, ForeignKey('tournaments.id'))
    player_id = Column(Integer, ForeignKey('players.id'))
    total = Column(Integer)

    tournament = relationship('Tournament', back_populates='scores')
    player = relationship('Player', back_populates='scores')

    def __init__(self, tournament=None, player=None, total=None):
        self.tournament = tournament
        self.player = player
        self.total = total


class Match(Base):
    __tablename__ = 'matches'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tournament_id = Column(Integer, ForeignKey('tournaments.id'))
    player_one_id = Column(Integer, ForeignKey('players.id'))
    player_two_id = Column(Integer, ForeignKey('players.id'))
    current_winner = Column(String(1))

    tournament = relationship('Tournament', back_populates='matches')
    player_one = relationship('Player', foreign_keys=player_one_id,
                              back_populates='o_matches')
    player_two = relationship('Player', foreign_keys=player_two_id,
                              back_populates='x_matches')
    logs = relationship('MatchLog', back_populates='match',
                        order_by='desc(MatchLog.timestamp)')

    UniqueConstraint(tournament_id, player_one_id, player_two_id)

    def __init__(self, tournament=None, player_one=None, player_two=None,
                 winner=None):
        self.tournament = tournament
        self.player_one = player_one
        self.player_two = player_two
        self.current_winner = winner

    def __repr__(self):
        return '<Match %r>' % self.id


class MatchLog(Base):
    __tablename__ = 'match_logs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    match_id = Column(Integer, ForeignKey('matches.id'))
    winner = Column(String(1))
    log = Column(Text)
    timestamp = Column(DateTime(timezone=True), default=func.now())

    match = relationship('Match', back_populates='logs')

    # UniqueConstraint(match_id, log)

    def __init__(self, match=None,  winner=None, log=None):
        self.match = match
        self.winner = winner
        self.log = log
