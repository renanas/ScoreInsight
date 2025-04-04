from sqlalchemy import Column, Integer, String, Float
from config.db_setup import Base

class Coach(Base):
    __tablename__ = 'coach'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_sofascore = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    nationality = Column(String)
    games_played = Column(Integer)
    performance = Column(String)
    points = Column(Integer)
    formation = Column(String)
    age = Column(Integer)