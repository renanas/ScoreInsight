import psycopg2
from psycopg2 import sql

def get_connection():
    """
    Retorna uma conexão com o banco de dados PostgreSQL.
    """
    try:
        connection = psycopg2.connect(
            dbname="score_insight",  # Nome do banco de dados
            user="postgres",         # Usuário do banco
            password="giovanna",     # Senha do banco
            host="localhost",        # Host do banco (use o IP público se for remoto)
            port="5432"              # Porta padrão do PostgreSQL
        )
        return connection
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None