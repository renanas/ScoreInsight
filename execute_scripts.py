from config.db_setup import Base, engine
from models import Coach, Club, Tournament, TournamentClub  # Importe todas as models necessárias

def create_tables():
    """
    Cria todas as tabelas no banco de dados PostgreSQL.
    """
    try:
        Base.metadata.create_all(engine)
        print("Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")

def drop_tables():
    """
    Exclui todas as tabelas do banco de dados PostgreSQL.
    """
    try:
        Base.metadata.drop_all(engine)
        print("Tabelas excluídas com sucesso!")
    except Exception as e:
        print(f"Erro ao excluir tabelas: {e}")

if __name__ == "__main__":
    # Escolha a operação que deseja realizar
    #action = input("Digite 'create' para criar tabelas ou 'drop' para excluir tabelas: ").strip().lower()

    #if action == "create":
    create_tables()
    #elif action == "drop":
    #drop_tables()
    #else:
     #   print("Ação inválida. Digite 'create' ou 'drop'.")