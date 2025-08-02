from sqlalchemy import Column, Integer, String
from config.db_setup import Base

from sqlalchemy.orm import relationship
from config.db_setup import Base

class Game(Base):
    __tablename__ = 'game'

    id = Column(String, primary_key=True)
    link = Column(String, nullable=False)
    info = Column(String, nullable=False)
    actions = Column(String, nullable=False)
    statistics = Column(String, nullable=False)
    time_home = Column(String, nullable=True)
    time_away = Column(String, nullable=True)