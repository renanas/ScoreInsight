import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import requests

def click_last_game(driver):
    """
    Localiza e clica no último jogo jogado pelo time.
    """
    try:
        get_all_games(driver)
    except Exception as e:
        print(f"Erro ao clicar no último jogo: {e}")
        
def get_all_games(driver):
    """
    Captura os hrefs de todos os jogos e navega para cada um deles, esperando 2 segundos em cada página.
    
    Args:
        driver: Instância do Selenium WebDriver.
    """
    try:
         # Busca todos os jogos dentro do bloco de partidas
        games = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((
                By.XPATH,
                "//div[contains(@class, 'Box Flex ggRYVx iWGVcA')]//a[contains(@href, '/pt/football/match/')]"
            ))
        )
        if games:
            first_link = games[0].get_attribute("href")
            print(f"Primeiro link de jogo encontrado: {first_link}")
            driver.get(first_link)
            time.sleep(2)  # Esperar 2 segundos
            #get_game_info(driver)
            #get_game_minute_for_minute(driver)
            get_statistic_game_overview_by_link(driver, first_link)
            return first_link            
        else:
            print("Nenhum jogo encontrado.")
                      

    except Exception as e:
        print(f"Erro ao navegar pelos jogos: {e}")

def get_game_info(driver):
    """
    Captura as informações de um jogo na página atual.
    
    Args:
        driver: Instância do Selenium WebDriver.
    
    Returns:
        Um dicionário contendo as informações do jogo.
    """
    try:
        # Capturar a data e hora da partida
        date_time_element = driver.find_element(By.XPATH, "//div[@class='d_flex ai_center br_lg bg-c_surface.s2 py_xs px_sm mb_xs h_[26px]']")
        date_time_text = date_time_element.text.split("\n")  # Exemplo: "05/03/2025\n17:00"
        game_date = date_time_text[0].strip()
        game_time = date_time_text[1].strip()

        # Capturar os nomes dos times
        left_team_element = driver.find_element(By.XPATH, "//div[@data-testid='left_team']//bdi")
        right_team_element = driver.find_element(By.XPATH, "//div[@data-testid='right_team']//bdi")
        left_team_name = left_team_element.text.strip()
        right_team_name = right_team_element.text.strip()

        # Capturar o resultado do jogo
        left_score_element = driver.find_element(By.XPATH, "//span[@data-testid='left_score']")
        right_score_element = driver.find_element(By.XPATH, "//span[@data-testid='right_score']")
        left_score = left_score_element.text.strip()
        right_score = right_score_element.text.strip()

        # Capturar os gols (se houver)
        scorer_elements = driver.find_elements(By.XPATH, "//div[@data-testid='scorer_list']//span")
        scorers = [scorer.text.strip() for scorer in scorer_elements]

        # Retornar as informações como um dicionário
        game_info = {
            "date": game_date,
            "time": game_time,
            "left_team": left_team_name,
            "right_team": right_team_name,
            "left_score": left_score,
            "right_score": right_score,
            "scorers": scorers,
        }

        print("Informações do jogo capturadas:", game_info)
        return game_info

    except Exception as e:
        print(f"Erro ao capturar as informações do jogo: {e}")
        return {}
    

def get_game_minute_for_minute(driver):
    try:
        get_substitutions(driver)
    except Exception as e:
        print(f"Erro ao capturar as informações do jogo minuto a minuto: {e}")
        return {}
    

def get_substitutions(driver):
    """
    Captura os nomes dos jogadores envolvidos em substituições (times esquerdo e direito) e o minuto do evento.
    
    Args:
        driver: Instância do Selenium WebDriver.
    
    Returns:
        Uma lista de dicionários contendo os nomes dos jogadores e o minuto da substituição.
    """
    try:
        # Localizar todos os elementos de substituições
        substitution_elements = driver.find_elements(By.XPATH, "//div[@cursor='pointer' and contains(@class, 'Box cbmnyx')]")
        
        substitutions = []
        for substitution in substitution_elements:
            try:
                # Capturar o minuto do evento
                minute_element = substitution.find_element(By.XPATH, ".//div[contains(@class, 'Text falluO')]")
                minute = minute_element.text.strip()

                # Capturar os jogadores do time esquerdo
                player_elements_left = substitution.find_elements(By.XPATH, ".//span[contains(@class, 'Text dGsLCg') or contains(@class, 'Text iBaaGe')]")
                players_left = [player.text.strip() for player in player_elements_left]

                # Capturar os jogadores do time direito
                player_elements_right = substitution.find_elements(By.XPATH, ".//span[contains(@class, 'Text isFvDP') or contains(@class, 'Text dgNapt')]")
                players_right = [player.text.strip() for player in player_elements_right]

                # Adicionar substituições do time esquerdo
                if len(players_left) == 2:
                    substitutions.append({
                        "minute": minute,  # Minuto do evento
                        "team": "left",  # Time esquerdo
                        "player_out": players_left[1],  # Jogador que saiu
                        "player_in": players_left[0],  # Jogador que entrou
                    })

                # Adicionar substituições do time direito
                if len(players_right) == 2:
                    substitutions.append({
                        "minute": minute,  # Minuto do evento
                        "team": "right",  # Time direito
                        "player_out": players_right[1],  # Jogador que saiu
                        "player_in": players_right[0],  # Jogador que entrou
                    })
            except Exception as e:
                print(f"Erro ao capturar uma substituição: {e}")
                continue

        print("Substituições capturadas:", substitutions)
        return substitutions

    except Exception as e:
        print(f"Erro ao capturar substituições: {e}")
        return [] 

def get_statistic_game_overview_by_link(driver, first_game_link):
    """
    Gera a URL de estatísticas com base no ID extraído do link do jogo e faz a requisição com headers e cookies.
    
    Args:
        driver: Instância do Selenium WebDriver.
        first_game_link: URL do jogo (string).
    
    Returns:
        Dados de estatísticas ou None em caso de erro.
    """
    try:
        time.sleep(1)
        # Extrair o ID do jogo da primeira string
        game_id = first_game_link.split("#id:")[-1]
        
        # Construir a URL de estatísticas
        statistics_url = f"http://www.sofascore.com/api/v1/event/{game_id}/statistics"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
        }


        response = requests.get(statistics_url, headers=headers)

        print(response.status_code)
        
        data = response.json()
        all_data = []
        
        for match_data in data['statistics']:
            period = match_data['period']

            for group in match_data['groups']:
                group_name = group['groupName']

                for item in group['statisticsItems']:
                    item_name = item.get('name')
                    home_team = item.get('home')
                    away_team = item.get('away')

                    all_data.append({
                        "period": period,
                        "group_name": group_name,
                        "item_name": item_name,
                        "home_team_value": home_team,
                        "away_team_value": away_team
                    })
        
        # Printar os dados capturados
        for item in all_data:
            print(f"Período: {item['period']}, Grupo: {item['group_name']}, Item: {item['item_name']}, Time da Casa: {item['home_team_value']}, Time de Fora: {item['away_team_value']}")

    except Exception as e:
        print(f"Erro ao gerar a URL de estatísticas: {e}")
        return None