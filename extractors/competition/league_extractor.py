from extractors.competition.competition_extractor import select_competition
from utils import helpers
from utils.helpers import click_element
from utils.constants import (
    LEAGUE_BUTTOM_COMPETITION,
    LEAGUE_TEAM_POSITION,
    LEAGUE_TEAM_INFO,
    LEAGUE_TEAM_INFO_2,
    LEAGUE_TEAM_INFO_LAST_GAMES,
)
from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def extract_team_league(driver, teams, team_stats, team_name, league_name="Liga dos Campeões da UEFA"):
    """
    Extrai as estatísticas do time para uma liga específica.
    
    Args:
        driver: Instância do Selenium WebDriver.
        team_stats: Objeto TeamStats para armazenar as estatísticas.
        league_name: Nome da liga a ser selecionada (ex: "LaLiga").
    """
    try:
        # Clicar no botão da liga para abrir o menu
        helpers.click_element(driver, LEAGUE_BUTTOM_COMPETITION)
        time.sleep(1)

        # Selecionar a liga desejada
        select_competition(driver, league_name)
        time.sleep(0.5)

        team_xpath = teams[team_name]

        # Extrair Extrair informações do time na liga em Todos os jogos
        extract_team_league_position(driver, team_xpath, team_stats, "Todos")
        time.sleep(0.5)

        # Extrair informações do time na liga apenas dos jogos em Casa
        helpers.click_element(driver, "/html/body/div[1]/main/div[2]/div/div[2]/div[1]/div[2]/div[1]/div[3]/div[1]/div[2]")
        time.sleep(0.5)
        extract_team_league_position(driver, team_xpath, team_stats, "Casa")

        # Extrair informações do time na liga apenas dos jogos como Visitante
        helpers.click_element(driver, "/html/body/div[1]/main/div[2]/div/div[2]/div[1]/div[2]/div[1]/div[3]/div[1]/div[3]")
        time.sleep(0.5)
        extract_team_league_position(driver, team_xpath, team_stats, "Visitante")

    except Exception as e:
        print(f"Erro ao extrair estatísticas da liga: {e}")

def extract_team_league_position(driver, team_xpath, team_stats, field, category="League Position"):
    """
    Extrai informações da posição do time na liga.
    """
    try:
        parsed_url = urlparse(team_xpath)
        team_xpath_path = parsed_url.path

        team_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//a[@href='{team_xpath_path}']"))
        )

        # Extrair estatísticas
        position = team_element.find_element(By.XPATH, LEAGUE_TEAM_POSITION).text
        games = team_element.find_elements(By.XPATH, LEAGUE_TEAM_INFO)[0].text
        wins = team_element.find_elements(By.XPATH, LEAGUE_TEAM_INFO)[1].text
        draws = team_element.find_elements(By.XPATH, LEAGUE_TEAM_INFO)[2].text
        losses = team_element.find_elements(By.XPATH, LEAGUE_TEAM_INFO)[3].text
        goal_diff = team_element.find_elements(By.XPATH, LEAGUE_TEAM_INFO_2)[0].text
        goals = team_element.find_elements(By.XPATH, LEAGUE_TEAM_INFO_2)[1].text
        points = team_element.find_elements(By.XPATH, LEAGUE_TEAM_INFO)[-1].text

        # Adicionar estatísticas ao objeto TeamStats
        team_stats.add_stat(f"{category} - {field}", "Posição", position)
        team_stats.add_stat(f"{category} - {field}", "Jogos", games)
        team_stats.add_stat(f"{category} - {field}", "Vitórias", wins)
        team_stats.add_stat(f"{category} - {field}", "Empates", draws)
        team_stats.add_stat(f"{category} - {field}", "Derrotas", losses)
        team_stats.add_stat(f"{category} - {field}", "Saldo de Gols", goal_diff)
        team_stats.add_stat(f"{category} - {field}", "Gols Marcados/Sofridos", goals)
        team_stats.add_stat(f"{category} - {field}", "Pontuação", points)

        # Extrair os últimos jogos (resultados e títulos)
        last_matches = team_element.find_elements(By.XPATH, LEAGUE_TEAM_INFO_LAST_GAMES)
        match_results = []
        for match in last_matches:
            title = match.get_attribute("title")  # Extrair o título do jogo
            result = match.find_element(By.XPATH, ".//span").text  # Extrair o resultado (D, V ou E)
            match_results.append({"title": title, "result": result})

        # Adicionar os últimos jogos ao objeto TeamStats
        team_stats.add_stat(f"{category} - {field}", "Últimos Jogos", match_results)

        print(f"Informações da posição na liga extraídas com sucesso no contexto '{field}'.")
        time.sleep(2)

    except Exception as e:
        print(f"Erro ao extrair informações da posição na liga: {e}")
