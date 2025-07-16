from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from config.db_setup import Base

# Modelo para a tabela Tournament
class Game(Base):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True)
    link = Column(String, nullable=False)
    info = Column(String, nullable=False)
    actions = Column(String, nullable=False)
    statistics = Column(String, nullable=False)