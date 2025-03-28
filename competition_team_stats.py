from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
from dto.teamStats import TeamStats
from utils.constants import  (
    REAL_MADRID_XPATH,
    LIGA_BUTTOM_STATISTIC_SESSION,
    POSITION_SCORE_ALL_XPATH_BASE,
    RESUME_XPATH_INFO,
    ATTACK_BUTTOM_STATISTIC_SESSION,
    ATTACK_XPATH_INFO,
    PASSE_BUTTOM_STATISTIC_SESSION,
    PASSE_XPATH_INFO,
    DEFENDING_BUTTOM_STATISTIC_SESSION,
    DEFENDING_XPATH_INFO,
    OTHERS_BUTTOM_STATISTIC_SESSION,
    OTHERS_XPATH_INFO,
    LEAGUE_BUTTOM_COMPETITION,
    LEAGUE_COMPETITION,
    LEAGUE_TEAM_POSITION,
    LEAGUE_TEAM_INFO,
    LEAGUE_TEAM_INFO_2,
    LEAGUE_TEAM_INFO_LAST_GAMES,
    BARCELONA_XPATH,
)

import time

def setup_driver():
    """Configura o driver do Selenium."""
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver

def click_element(driver, xpath, timeout=10):
    """Espera até que o elemento esteja clicável e clica nele."""
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    element.click()

def navigate_to_team_page(driver, team_name, teams):
    """Navega para a página do time especificado."""
    url = teams[team_name]
    driver.get(url)
    time.sleep(5)  # Esperar a página carregar completamente

def extract_stats(driver, xpath_base, num_elements, category, team_stats):
    try:
        stats_element = driver.find_element(By.XPATH, xpath_base)
        for i in range(1, num_elements + 1):
            key_xpath = f'{xpath_base}/div[{i}]/span[1]'
            value_xpath = f'{xpath_base}/div[{i}]/span[2]'
            key = stats_element.find_element(By.XPATH, key_xpath).text
            value = stats_element.find_element(By.XPATH, value_xpath).text
            team_stats.add_stat(category, key, value)
    except Exception as e:
        print(f"Erro ao encontrar o elemento: {e}")

def extract_position(driver, position_all_xpath_base, category, team_stats):
    try:
        value = driver.find_element(By.XPATH, position_all_xpath_base).text
        key = "classificacao"
        team_stats.add_stat(category, key, value)
    except Exception as e:
        print(f"Erro ao encontrar o elemento: {e}")
        driver.save_screenshot('error_screenshot.png')

def extract_team_stats(driver, team_stats, competition_name="Liga dos Campeões da UEFA"):
    """Extrai as estatísticas do time para uma competição específica."""
    # Clicar no botão da liga
    click_element(driver, LIGA_BUTTOM_STATISTIC_SESSION)
    time.sleep(1)

    # Selecionar a competição desejada
    select_competition(driver, competition_name)
    time.sleep(0.5)

    # Extrair posição e pontuação do SofaScore
    extract_position(driver, POSITION_SCORE_ALL_XPATH_BASE, "Position/Score", team_stats)

    # Extrair estatísticas de RESUMO
    extract_stats(driver, RESUME_XPATH_INFO, 4, "Resumo", team_stats)

    # Clicar no botão de ATAQUE e extrair estatísticas
    click_element(driver, ATTACK_BUTTOM_STATISTIC_SESSION)
    time.sleep(0.5)
    extract_stats(driver, ATTACK_XPATH_INFO, 19, "Ataque", team_stats)

    # Clicar no botão de PASSE e extrair estatísticas
    click_element(driver, PASSE_BUTTOM_STATISTIC_SESSION)
    time.sleep(0.5)
    extract_stats(driver, PASSE_XPATH_INFO, 6, "Passe", team_stats)

    # Clicar no botão de DEFENDENDO e extrair estatísticas
    click_element(driver, DEFENDING_BUTTOM_STATISTIC_SESSION)
    time.sleep(0.5)
    extract_stats(driver, DEFENDING_XPATH_INFO, 13, "Defendendo", team_stats)

    # Clicar no botão de OUTROS e extrair estatísticas
    click_element(driver, OTHERS_BUTTOM_STATISTIC_SESSION)
    time.sleep(0.5)
    extract_stats(driver, OTHERS_XPATH_INFO, 10, "Outros", team_stats)
    time.sleep(2)

def select_competition(driver, competition_name):
    """
    Seleciona a competição desejada no menu de competições.
    
    Args:
        driver: Instância do Selenium WebDriver.
        competition_name: Nome da competição a ser selecionada (ex: "Liga dos Campeões da UEFA").
    """
    try:
        # Localizar todas as opções de competições
        competition_options = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, ".//li[@role='option']"))
        )
        
        # Percorrer as opções e selecionar a competição desejada
        for option in competition_options:
            print('Vezes que passou aqui')
            competition_text = option.find_element(By.XPATH, ".//bdi").text
            if competition_text == competition_name:
                option.click()
                print(f"Competição '{competition_name}' selecionada com sucesso.")
                return

        print(f"Competição '{competition_name}' não encontrada.")
    except Exception as e:
        print(f"Erro ao selecionar a competição: {e}")



def extract_team_league(driver, team_stats, league_name="Liga dos Campeões da UEFA"):
    """
    Extrai as estatísticas do time para uma liga específica.
    
    Args:
        driver: Instância do Selenium WebDriver.
        team_stats: Objeto TeamStats para armazenar as estatísticas.
        league_name: Nome da liga a ser selecionada (ex: "LaLiga").
    """
    try:
        # Clicar no botão da liga para abrir o menu
        click_element(driver, LEAGUE_BUTTOM_COMPETITION)
        time.sleep(1)

        # Selecionar a liga desejada
        select_competition(driver, league_name)
        time.sleep(1)

        # Extrair posição e estatísticas do time na liga
        extract_team_league_position(driver, REAL_MADRID_XPATH, team_stats)

    except Exception as e:
        print(f"Erro ao extrair estatísticas da liga: {e}")

def extract_team_league_position(driver, team_xpath, team_stats, category="League Position"):
    """
    Extrai informações da posição do time na liga, incluindo:
    posição, jogos, vitórias, empates, derrotas, saldo de gols, gols marcados/sofridos e pontuação.
    """
    try:
        time.sleep(2)
        # Extrair apenas o caminho da URL (ex: /pt/time/futebol/real-madrid/2829)
        parsed_url = urlparse(team_xpath)
        team_xpath_path = parsed_url.path

        # Localizar o elemento do time na tabela da liga
        team_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//a[@href='{team_xpath_path}']"))
        )

        # Extrair as informações desejadas
        position = team_element.find_element(By.XPATH, LEAGUE_TEAM_POSITION).text
        games = team_element.find_elements(By.XPATH, LEAGUE_TEAM_INFO)[0].text
        wins = team_element.find_elements(By.XPATH, LEAGUE_TEAM_INFO)[1].text
        draws = team_element.find_elements(By.XPATH, LEAGUE_TEAM_INFO)[2].text
        losses = team_element.find_elements(By.XPATH, LEAGUE_TEAM_INFO)[3].text
        goal_diff = team_element.find_elements(By.XPATH, LEAGUE_TEAM_INFO_2)[0].text
        goals = team_element.find_elements(By.XPATH, LEAGUE_TEAM_INFO_2)[1].text
        points = team_element.find_elements(By.XPATH, LEAGUE_TEAM_INFO)[-1].text

        # Adicionar as informações ao objeto TeamStats
        team_stats.add_stat(category, "Posição", position)
        team_stats.add_stat(category, "Jogos", games)
        team_stats.add_stat(category, "Vitórias", wins)
        team_stats.add_stat(category, "Empates", draws)
        team_stats.add_stat(category, "Derrotas", losses)
        team_stats.add_stat(category, "Saldo de Gols", goal_diff)
        team_stats.add_stat(category, "Gols Marcados/Sofridos", goals)
        team_stats.add_stat(category, "Pontuação", points)

        # Extrair os últimos jogos (resultados e títulos)
        last_matches = team_element.find_elements(By.XPATH, LEAGUE_TEAM_INFO_LAST_GAMES)
        match_results = []
        for match in last_matches:
            title = match.get_attribute("title")  # Extrair o título do jogo
            result = match.find_element(By.XPATH, ".//span").text  # Extrair o resultado (D ou V)
            match_results.append({"title": title, "result": result})

        # Adicionar os últimos jogos ao objeto TeamStats
        team_stats.add_stat(category, "Últimos Jogos", match_results)

        print(f"Informações da posição na liga extraídas com sucesso para {team_xpath}.")
        time.sleep(2)

    except Exception as e:
        print(f"Erro ao extrair informações da posição na liga: {e}")

def main():
    """Fluxo principal do script."""
    driver = setup_driver()
    team_stats = TeamStats()

    try:
        teams = {"Barcelona": BARCELONA_XPATH}
        team_name = "Barcelona"

        # Navegar para a página do time
        navigate_to_team_page(driver, team_name, teams)

         # Extrair estatísticas do time na liga
        extract_team_league(driver, team_stats)

        # Extrair estatísticas do time
        extract_team_stats(driver, team_stats)

        # Exibir as estatísticas coletadas
        team_stats.display_stats()       

    finally:
        # Fechar o navegador
        driver.quit()


if __name__ == "__main__":
    main()