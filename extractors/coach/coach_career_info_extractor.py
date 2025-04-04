import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_coach_stats(driver):    
    """
    Extrai as estatísticas do técnico da página, incluindo:
    - Nome do técnico
    - Nacionalidade
    - Idade
    - Formação favorita
    - Número de jogos
    - Pontos por jogo
    
    """
    try:
        # Localizar o elemento do nome do técnico pelo XPath
        coach_name_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[@class='Text equVkn']"))
        )
        
        # Extrair o texto do elemento
        coach_name = coach_name_element.text
        print(f"Nome do técnico extraído com sucesso: {coach_name}")

        # Extrair nacionalidade
        nationality_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[text()='Nacionalidade']/following-sibling::div"))
        )
        nationality = nationality_element.text
        print(f"Nacionalidade: {nationality}")

        # Extrair idade
        age_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'anos')]"))
        )        
        age = age_element.text
        print(f"Idade: {age}")

        # Extrair formação favorita
        formation_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[text()='Formação fav.']/following-sibling::div"))
        )
        formation = formation_element.text
        print(f"Formação favorita: {formation}")

        # Extrair número de jogos
        games_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[text()='Jogos']/following-sibling::div"))
        )
        games = games_element.text
        print(f"Jogos: {games}")

        # Extrair pontos por jogo
        points_per_game_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[text()='Pontos/Jogo']/following-sibling::div"))
        )
        points_per_game = points_per_game_element.text
        print(f"Pontos por jogo: {points_per_game}")

        extract_performance_stats(driver)

        return coach_name
    except Exception as e:
        print(f"Erro ao extrair as estatísticas do técnico: {e}")
        return None

def extract_performance_stats(driver):
    """
    Extrai as estatísticas de desempenho de toda a carreia do técnico, incluindo:
    - Quantidade de vitórias, derrotas e empates.
    
    Args:
        driver: Instância do Selenium WebDriver.
    
    Returns:
        Um dicionário contendo as estatísticas de desempenho.
    """
    try:
        # Localizar a quantidade de vitórias
        wins_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='Box laShVk']//span[@color='secondary.default']"))
        )
        wins = wins_element.text
        print(f"Vitorias: {wins}")
        
        # Localizar a quantidade de derrotas
        losses_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='Box laShVk']//span[@color='error.default']"))
        )
        losses = losses_element.text
        print(f"Derrotas: {losses}")

        # Localizar a quantidade de empates
        draws_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='Box laShVk']//span[@color='onSurface.nLv3']"))
        )
        draws = draws_element.text
        print(f"Empates: {draws}")

        # Retornar os resultados como um dicionário
        return {
            "wins": {"quantity": wins},
            "losses": {"quantity": losses},
            "draws": {"quantity": draws},
        }
    except Exception as e:
        print(f"Erro ao extrair as estatísticas de desempenho: {e}")
        return None