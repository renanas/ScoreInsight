from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from config.db_setup import Base

class CoachClub(Base):
    __tablename__ = 'coach_club'

    id = Column(Integer, primary_key=True, autoincrement=True)
    coach_id = Column(Integer, ForeignKey('coach.id'), nullable=False)  # Chave estrangeira para a tabela coach
    club_id = Column(Integer, ForeignKey('club.id'), nullable=False)    # Chave estrangeira para a tabela club
    games_played = Column(Integer)
    victories = Column(Integer)
    draws = Column(Integer)
    defeats = Column(Integer)
    points = Column(Integer)

    # Relacionamentos
    coach = relationship('Coach', backref='coach_clubs')  # Relacionamento com a tabela Coach
    club = relationship('Club', backref='coach_clubs')    # Relacionamento com a tabela Club