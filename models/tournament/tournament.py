from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from config.db_setup import Base

# Modelo para a tabela Tournament
class Tournament(Base):
    __tablename__ = 'tournament'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)