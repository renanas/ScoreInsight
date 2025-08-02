import time
import json
from models.game.game import Game
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from repository.game_repository import save_game
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
            driver.get(first_link)
            time.sleep(2)  
            game_info = get_game_info(driver)
            game_minute_actions = get_game_minute_for_minute(driver)
            game_statistic_overview = get_statistic_game_overview_by_link(driver, first_link)
            game_id = first_link.split("#id:")[-1]
            
            info_str = json.dumps(game_info, ensure_ascii=False)
            actions_str = json.dumps(game_minute_actions, ensure_ascii=False)
            statistics_str = json.dumps(game_statistic_overview, ensure_ascii=False)

            game = Game(
                    id=game_id,
                    link=first_link,
                    info=info_str,
                    actions=actions_str,
                    statistics=statistics_str,
                    time_home=game_info.get("left_team"),
                    time_away=game_info.get("right_team")
                )
            
            print(f"Jogo capturado: {game.id}, Link: {game.link}")

            save_game(game)
            
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
        # Nome dos times
        left_team = driver.find_element(By.XPATH, "//bdi[1]").text.strip()
        right_team = driver.find_element(By.XPATH, "//bdi[2]").text.strip()

        # Placar
        scores = driver.find_elements(By.XPATH, "//span[contains(@class, 'textStyle_display.extraLarge')]")
        left_score = scores[0].text.strip() if len(scores) > 0 else ""
        right_score = scores[2].text.strip() if len(scores) > 1 else ""

        # Goleadores do time da esquerda
        left_scorers = [span.text.strip() for span in driver.find_elements(
            By.XPATH, "//div[contains(@class, 'ai_flex-end')]//span[contains(@class, 'textStyle_body.small')]"
        )]

        # Goleadores do time da direita
        right_scorers = [span.text.strip() for span in driver.find_elements(
            By.XPATH, "//div[contains(@class, 'ai_flex-start')]//span[contains(@class, 'textStyle_body.small')]"
        )]
        print(f"Left scorers: {left_scorers}")

        set_left = set(left_scorers)
        set_right = set(right_scorers)  

        # Pega apenas os nomes únicos de cada lado
        unique_left = list(set_left)
        unique_right = list(set_right - set_left)

        print(f"Time da esquerda: {left_team}, Placar: {left_score}")
        print(f"Time da direita: {right_team}, Placar: {right_score}")
        print(f"Goleadores únicos do time da esquerda: {unique_left}")
        print(f"Goleadores únicos do time da direita: {unique_right}")

        return {
            "left_team": left_team,
            "right_team": right_team,
            "left_score": left_score,
            "right_score": right_score,
            "left_scorers": left_scorers,
            "right_scorers": right_scorers,
        }
    except Exception as e:
        print(f"Erro ao extrair informações do jogo: {e}")
        return {}
    

def get_game_minute_for_minute(driver):
    try:
        eventos = extract_all_events_from_all_blocks(driver)
        for evento in eventos:
            print(evento) 
            
        return eventos 
        
    except Exception as e:
        print(f"Erro ao capturar as informações do jogo minuto a minuto: {e}")
        return {}
    
def extract_all_events_from_all_blocks(driver):
    """
    Extrai todos os eventos de todos os blocos <div class="pb_sm"> da página.
    Retorna uma lista de dicionários com minuto, tipo, jogadores e descrição.
    """
    all_events = []
    # Encontra todos os blocos de eventos
    blocks = driver.find_elements(By.XPATH, "//div[contains(@class, 'pb_sm')]")
    for block in blocks:
        event_blocks = block.find_elements(By.XPATH, ".//div[contains(@class, 'hover:bg_surface.s2')]")
        for event in event_blocks:
            try:
                # Minuto
                minute = ""
                try:
                    minute = event.find_element(By.XPATH, ".//span[contains(@class, 'textStyle_display.micro')]").text.strip()
                except Exception:
                    pass

                # Tipo do evento (svg/title)
                event_type = ""
                try:
                    svg = event.find_element(By.XPATH, ".//svg")
                    event_type = svg.find_element(By.XPATH, "./title").get_attribute("textContent").strip()
                except Exception:
                    pass

                # Jogadores e descrição (spans)
                players = []
                description = ""
                spans = event.find_elements(By.XPATH, ".//span[contains(@class, 'textStyle_body.medium')]")
                if len(spans) == 1:
                    players = [spans[0].text.strip()]
                elif len(spans) >= 2:
                    players = [spans[0].text.strip()]
                    description = spans[1].text.strip()
                    # Substituição: normalmente dois jogadores
                    if "Substituição" in event_type or (len(spans) > 2 and spans[2].text.strip()):
                        players = [spans[0].text.strip(), spans[1].text.strip()]
                        description = "Substituição"

                # Se description estiver vazio, tenta pegar do svg
                if not description and event_type:
                    description = event_type

                all_events.append({
                    "minute": minute,
                    "type": event_type,
                    "players": players,
                    "description": description
                })
            except Exception as e:
                print(f"Erro ao processar evento: {e}")
                continue
    return all_events

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
        return all_data

    except Exception as e:
        print(f"Erro ao gerar a URL de estatísticas: {e}")
        return None