from dto.team_stats import TeamStats
from extractors.league_extractor import extract_team_league
from extractors.stats_extractor import extract_team_resume_session_stats
from utils import helpers
from utils.constants import  (
    REAL_MADRID_XPATH,
    BARCELONA_XPATH,
)

def main():
    """Fluxo principal do script."""
    driver = helpers.setup_driver()
    team_stats = TeamStats()

    try:
        teams = {
            "Barcelona": BARCELONA_XPATH,
            "Real Madrid": REAL_MADRID_XPATH
        }
        team_name = "Barcelona"

        # Navegar para a página do time
        helpers.navigate_to_team_page(driver, team_name, teams)

        # Extrair estatísticas do time na liga
        extract_team_league(driver, teams, team_stats, team_name)

        # Extrair estatísticas de resumo do time
        extract_team_resume_session_stats(driver, team_stats)

        # Exibir as estatísticas coletadas
        team_stats.display_stats()       

    finally:
        # Fechar o navegador
        driver.quit()


if __name__ == "__main__":
    main()