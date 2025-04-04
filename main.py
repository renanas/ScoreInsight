from dto.team_stats import TeamStats
from extractors.coach_extractor import extract_coach
from extractors.league_extractor import extract_team_league
from extractors.stats_extractor import extract_team_resume_session_stats
from utils import helpers
from utils.constants import  (
    BAYERN_MUNICH_XPATH,
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

    # Flags para controle de extração
    flag_to_extract_league = False  # Define se deseja extrair estatísticas da liga
    flag_to_extract_resume_session = False  # Define se deseja extrair estatísticas de resumo da sessão
    flag_to_extract_coach = True  # Define se deseja extrair estatísticas do treinador
    try:
        teams = {
            "Barcelona": BARCELONA_XPATH,
            "Real Madrid": REAL_MADRID_XPATH,
            "Bayern Munich": BAYERN_MUNICH_XPATH,
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

        # Exibir as estatísticas coletadas
        # team_stats.display_stats()       

    finally:
        # Fechar o navegador
        driver.quit()


if __name__ == "__main__":
    main()