from dto.team_stats import TeamStats
from extractors.coach.coach_extractor import extract_coach
from extractors.competition.league_extractor import extract_team_league
from extractors.competition.stats_extractor import extract_team_resume_session_stats
from extractors.games.last_games_extractor import click_last_game
from utils import helpers
from utils.constants import  (
    BAYERN_MUNCHEN_XPATH,
    REAL_MADRID_XPATH,
    BARCELONA_XPATH,
)
from config.db_setup import Base, engine
from models import Coach, Club, Tournament, TournamentClub  # Importe todos os modelos que você criou


def create_tables():
    """
    Cria todas as tabelas no banco de dados.
    """
    Base.metadata.create_all(engine)
    print("Tabelas criadas com sucesso!")

def main():
    """Fluxo principal do script."""
    driver = helpers.setup_driver()
    team_stats = TeamStats()
    create_tables()

    # Flags para controle de extração
    flag_to_extract_league = False  
    flag_to_extract_resume_session = False  
    flag_to_extract_coach = False  
    flag_to_extract_last_matchs = True  
    try:
        teams = {
            "Barcelona": BARCELONA_XPATH,
            "Real Madrid": REAL_MADRID_XPATH,
            "Bayern Munchen": BAYERN_MUNCHEN_XPATH,
        }

        team_name = "Barcelona"

        # Navegar para a página do time
        helpers.navigate_to_team_page(driver, team_name, teams)

        # Extrair estatísticas do time na liga
        if flag_to_extract_league:
            # Extrair estatísticas do time na liga
            extract_team_league(driver, teams, team_stats, team_name)
        
        if flag_to_extract_resume_session:
            # Extrair estatísticas de resumo da sessão
            extract_team_resume_session_stats(driver, team_stats)

        if flag_to_extract_coach:
            # Extrair estatísticas do treinador
            extract_coach(driver, teams, team_name)

        if flag_to_extract_last_matchs:
            click_last_game(driver)

        # Exibir as estatísticas coletadas
        # team_stats.display_stats()       

    finally:
        # Fechar o navegador
        driver.quit()


if __name__ == "__main__":
    main()