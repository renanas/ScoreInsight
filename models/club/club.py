from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from config.db_setup import Base

class Club(Base):
    __tablename__ = 'club'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_sofascore = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    city = Column(String)
    date_foundation = Column(Date)
    coach = Column(Integer, ForeignKey('coach.id'))  # Relacionamento com a tabela Coach
    stadium = Column(String)
    xpath = Column(Text)

    # Relacionamento com o modelo Coach
    coach_relationship = relationship('Coach', backref='clubs')