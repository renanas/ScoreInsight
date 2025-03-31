from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Base para os modelos
Base = declarative_base()

# Configuração do banco de dados
DATABASE_URL = 'postgresql://postgres:giovanna@localhost:5432/score_insight'

# Criar o engine e a sessão
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()