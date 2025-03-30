from db_connection import get_connection

def test_db_connection():
    """Testa a conexão com o banco de dados."""
    connection = get_connection()
    if connection:
        print("Conexão com o banco de dados estabelecida com sucesso!")
        connection.close()
    else:
        print("Falha ao conectar ao banco de dados.")

if __name__ == "__main__":
    test_db_connection()