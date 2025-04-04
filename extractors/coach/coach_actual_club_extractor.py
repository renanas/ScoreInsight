import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_performance_stats_actual_club(driver, teams, team_name):
    """
    Extrai as informações do time atual, incluindo:
    - Nome do time
    - Quantidade de jogos
    - Quantidade de vitórias
    - Quantidade de empates
    - Quantidade de derrotas
    - Pontos por jogo
    
    Args:
        driver: Instância do Selenium WebDriver.
        teams: Dicionário contendo os times e seus respectivos XPaths.
        team_name: Nome do time a ser extraído.
    
    Returns:
        Um dicionário contendo as informações do time atual.
    """
    
    try:
        team_xpath = teams.get(team_name)
        if not team_xpath:
            print(f"Time '{team_name}' não encontrado no dicionário de times.")
            return None
        
        team_xpath = teams.get(team_name).replace("https://www.sofascore.com", "")
        team_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//a[@href='{team_xpath}']"))
        )
        
        team_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//a[@href='{team_xpath}']"))
        )
        if team_element:
            # Localizar o nome do time
            team_name_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//a[@href='{team_xpath}']//span[@class='Text ietnEf']"))
            )
            extracted_team_name = team_name_element.text
            print(f"Nome do time extraído com sucesso: {extracted_team_name}")
            
            # Localizar os pontos por jogo
            points_per_game_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//a[@href='{team_xpath}']//span[@class='Text hWjZUN']"))
            )
            points_per_game = points_per_game_element.text

            # Localizar a quantidade de jogos
            games_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//a[@href='{team_xpath}']//span[@class='Text gDzvPs']"))
            )
            games = games_element.text

            # Localizar a quantidade de vitórias
            wins_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//a[@href='{team_xpath}']//span[@class='Text cPtTWR']"))
            )
            wins = wins_element.text

            # Localizar a quantidade de empates
            draws_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//a[@href='{team_xpath}']//span[@class='Text gDWoTW']"))
            )
            draws = draws_element.text

            # Localizar a quantidade de derrotas
            losses_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//a[@href='{team_xpath}']//span[@class='Text cDomgH']"))
            )
            losses = losses_element.text

            # Exibir os resultados no console
            print(f"Nome do time: {extracted_team_name}")
            print(f"Jogos: {games}")
            print(f"Vitórias: {wins}")
            print(f"Empates: {draws}")
            print(f"Derrotas: {losses}")
            print(f"Pontos por jogo: {points_per_game}")

            # Retornar os resultados como um dicionário
            return {
                "team_name": extracted_team_name,
                "games": games,
                "wins": wins,
                "draws": draws,
                "losses": losses,
                "points_per_game": points_per_game,
            }
            
    except Exception as e:
        print(f"Erro ao extrair as informações do time: {e}")
        return None