from selenium.webdriver.common.by import By
from extractors.competition_extractor import select_competition
from utils import helpers
from utils.constants import  (
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
)

import time

def extract_team_resume_session_stats(driver, team_stats, competition_name="Liga dos Campeões da UEFA"):
    """Extrai as estatísticas do time para uma competição específica."""
    # Clicar no botão da liga
    helpers.click_element(driver, LIGA_BUTTOM_STATISTIC_SESSION)
    time.sleep(1)

    # Selecionar a competição desejada
    select_competition(driver, competition_name)
    time.sleep(0.5)

    # Extrair posição e pontuação do SofaScore
    extract_position(driver, POSITION_SCORE_ALL_XPATH_BASE, "Position/Score", team_stats)

    # Extrair estatísticas de RESUMO
    extract_resume_session_stats(driver, RESUME_XPATH_INFO, 4, "Resumo", team_stats)

    # Clicar no botão de ATAQUE e extrair estatísticas
    helpers.click_element(driver, ATTACK_BUTTOM_STATISTIC_SESSION)
    time.sleep(0.5)
    extract_resume_session_stats(driver, ATTACK_XPATH_INFO, 19, "Ataque", team_stats)

    # Clicar no botão de PASSE e extrair estatísticas
    helpers.click_element(driver, PASSE_BUTTOM_STATISTIC_SESSION)
    time.sleep(0.5)
    extract_resume_session_stats(driver, PASSE_XPATH_INFO, 6, "Passe", team_stats)

    # Clicar no botão de DEFENDENDO e extrair estatísticas
    helpers.click_element(driver, DEFENDING_BUTTOM_STATISTIC_SESSION)
    time.sleep(0.5)
    extract_resume_session_stats(driver, DEFENDING_XPATH_INFO, 13, "Defendendo", team_stats)

    # Clicar no botão de OUTROS e extrair estatísticas
    helpers.click_element(driver, OTHERS_BUTTOM_STATISTIC_SESSION)
    time.sleep(0.5)
    extract_resume_session_stats(driver, OTHERS_XPATH_INFO, 10, "Outros", team_stats)
    time.sleep(2)

def extract_position(driver, position_all_xpath_base, category, team_stats):
    try:
        value = driver.find_element(By.XPATH, position_all_xpath_base).text
        key = "classificacao"
        team_stats.add_stat(category, key, value)
    except Exception as e:
        print(f"Erro ao encontrar o elemento: {e}")
        driver.save_screenshot('error_screenshot.png')

def extract_resume_session_stats(driver, xpath_base, num_elements, category, team_stats):
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