from sqlalchemy import Column, Integer, String, Float
from config.db_setup import Base

class Coach(Base):
    __tablename__ = 'coach'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_sofascore = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    age = Column(Integer)
    nationality = Column(String)
    formation = Column(String)
    games_played = Column(Integer)
    victories = Column(Integer)
    draws = Column(Integer)
    defeats = Column(Integer)
    points = Column(Integer)
    
    