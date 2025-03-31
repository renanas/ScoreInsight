from sqlalchemy import Column, Integer, String, ForeignKey, Text
from config.db_setup import Base

# Modelo para a tabela Tournament_Club
class TournamentClub(Base):
    __tablename__ = 'tournament_club'

    club_id = Column(Integer, ForeignKey('club.id'), primary_key=True)
    tournament_id = Column(Integer, ForeignKey('tournament.id'), primary_key=True)
    position = Column(Integer)
    games_played = Column(Integer)
    wins = Column(Integer)
    draws = Column(Integer)
    losses = Column(Integer)
    goals_scored = Column(Integer)
    goals_conceded = Column(Integer)
    points = Column(Integer)
    last_games = Column(Text)
    season = Column(String, primary_key=True)

# Modelo para a tabela Tournament_Club_Home
class TournamentClubHome(Base):
    __tablename__ = 'tournament_club_home'

    club_id = Column(Integer, ForeignKey('club.id'), primary_key=True)
    tournament_id = Column(Integer, ForeignKey('tournament.id'), primary_key=True)
    position = Column(Integer)
    games_played = Column(Integer)
    wins = Column(Integer)
    draws = Column(Integer)
    losses = Column(Integer)
    goals_scored = Column(Integer)
    goals_conceded = Column(Integer)
    points = Column(Integer)
    last_games = Column(Text)
    season = Column(String, primary_key=True)

# Modelo para a tabela Tournament_Club_Visiting
class TournamentClubVisiting(Base):
    __tablename__ = 'tournament_club_visiting'

    club_id = Column(Integer, ForeignKey('club.id'), primary_key=True)
    tournament_id = Column(Integer, ForeignKey('tournament.id'), primary_key=True)
    position = Column(Integer)
    games_played = Column(Integer)
    wins = Column(Integer)
    draws = Column(Integer)
    losses = Column(Integer)
    goals_scored = Column(Integer)
    goals_conceded = Column(Integer)
    points = Column(Integer)
    last_games = Column(Text)
    season = Column(String, primary_key=True)