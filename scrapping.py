from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import pandas as pd
import time

from utils.constants import  (
    REAL_MADRID_XPATH,
    LIGA_BUTTOM_STATISTIC_SESSION,
    LIGA_SELECAO_STATISTIC_SESSION,
    POSITION_SCORE_ALL_XPATH_BASE,
    RESUME_XPATH_INFO,
    ATTACK_BUTTOM_STATISTIC_SESSION,
    ATTACK_XPATH_INFO,
    PASSE_BUTTOM_STATISTIC_SESSION,
    PASSE_XPATH_INFO,
)

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

def extract_stats(driver, xpath_base, num_elements, category):
    stats = {}
    try:
        stats_element = driver.find_element(By.XPATH, xpath_base)
        for i in range(1, num_elements + 1):
            key_xpath = f'{xpath_base}/div[{i}]/span[1]'
            value_xpath = f'{xpath_base}/div[{i}]/span[2]'
            key = stats_element.find_element(By.XPATH, key_xpath).text
            value = stats_element.find_element(By.XPATH, value_xpath).text
            stats[key] = value

        for key, value in stats.items():
            print(f"{key}: {value}")
        print(f"EXTRAÇÃO {category} DEU CERTO")
    except Exception as e:
        print(f"Erro ao encontrar o elemento: {e}")
        driver.save_screenshot('error_screenshot.png')
    return stats

def extract_position(driver, position_all_xpath_base, category):
    stats = {}
    try:
        value = driver.find_element(By.XPATH, position_all_xpath_base).text
        key = "classificacao"
        stats[key] = value

        for key, value in stats.items():
            print(f"{key}: {value}")
        print(f"EXTRAÇÃO {category} DEU CERTO")
    except Exception as e:
        print(f"Erro ao encontrar o elemento: {e}")
        driver.save_screenshot('error_screenshot.png')
    return stats

def extract_team_stats(driver):
    """Extrai as estatísticas do time."""
    # Clicar no botão da liga
    click_element(driver, LIGA_BUTTOM_STATISTIC_SESSION)
    time.sleep(2)

    # Selecionar a liga
    click_element(driver, LIGA_SELECAO_STATISTIC_SESSION)
    time.sleep(2)

    # Extrair posição e pontuação do SofaScore
    extract_position(driver, POSITION_SCORE_ALL_XPATH_BASE, "Position/Score")
    time.sleep(2)

    # Extrair estatísticas de Resumo da Temporada
    extract_stats(driver, RESUME_XPATH_INFO, 4, "Resumo")
    time.sleep(2)

    # Clicar no botão de ataque e extrair estatísticas da Temporada
    click_element(driver, ATTACK_BUTTOM_STATISTIC_SESSION)
    extract_stats(driver, ATTACK_XPATH_INFO, 19, "Ataque")
    time.sleep(2)

    # Clicar no botão de passe e extrair estatísticas
    click_element(driver, PASSE_BUTTOM_STATISTIC_SESSION)
    extract_stats(driver, PASSE_XPATH_INFO, 6, "Passe")
    time.sleep(2)


def main():
    """Fluxo principal do script."""
    driver = setup_driver()

    try:
        teams = {"Real Madrid": REAL_MADRID_XPATH}
        team_name = "Real Madrid"

        # Navegar para a página do time
        navigate_to_team_page(driver, team_name, teams)

        # Extrair estatísticas do time
        extract_team_stats(driver)

    finally:
        # Fechar o navegador
        driver.quit()


if __name__ == "__main__":
    main()