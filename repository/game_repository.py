from config.db_setup import SessionLocal
from models.game.game import Game

def save_game(game):
    """
    Salva um objeto Game no banco de dados usando uma nova sessão.
    """
    session = SessionLocal()
    try:
        session.add(game)
        session.commit()
        print(f"Jogo salvo no banco com id {game.id}")
    except Exception as e:
        session.rollback()
        print(f"Erro ao salvar jogo: {e}")
    finally:
        session.close()