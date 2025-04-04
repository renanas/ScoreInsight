import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_coach(driver, teams, team_name):
    """
    Clica no elemento do técnico (Hans-Dieter Flick) na página.
    """
    try:
        # Localizar o elemento pelo XPath
        time.sleep(2)  # Esperar o carregamento da página
        #driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2)")
        
        
        # Localizar o elemento do link do técnico pelo XPath
        coach_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Treinador']/following-sibling::div/a"))
        )
        # Clicar no elemento
        coach_element.click()
        time.sleep(2)

        # Extrair as estatísticas do técnico
        extract_coach_stats(driver, teams, team_name)

        print("Elemento do técnico clicado com sucesso!")
    except Exception as e:
        print(f"Erro ao clicar no elemento do técnico: {e}")

def extract_coach_stats(driver, teams, team_name):    
    """
    Extrai as estatísticas do técnico da página.
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

        #extract_performance_stats(driver)
        extract_performance_stats_actual_club(driver, teams, team_name)

        return coach_name
    except Exception as e:
        print(f"Erro ao extrair as estatísticas do técnico: {e}")
        return None

def extract_performance_stats(driver, teams):
    """
    Extrai as estatísticas de desempenho do técnico, incluindo:
    - Quantidade de vitórias, derrotas e empates.
    - Porcentagem de vitórias, derrotas e empates.
    
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
    print(f"Extraindo informações do time: {team_name}...")
    # Normalizar o href para lidar com URLs completas
    
    try:
        # Obter o XPath do time com base no nome fornecido
        team_xpath = teams.get(team_name)
        if not team_xpath:
            print(f"Time '{team_name}' não encontrado no dicionário de times.")
            return None
        
        team_xpath = teams.get(team_name).replace("https://www.sofascore.com", "")
        team_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//a[@href='{team_xpath}']"))
        )
        # Verificar se o time atual corresponde ao time no mapa
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