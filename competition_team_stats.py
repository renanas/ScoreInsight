from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from dto.teamStats import TeamStats
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
    DEFENDING_BUTTOM_STATISTIC_SESSION,
    DEFENDING_XPATH_INFO,
    OTHERS_BUTTOM_STATISTIC_SESSION,
    OTHERS_XPATH_INFO,
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

def extract_team_stats(driver, team_stats):
    """Extrai as estatísticas do time."""
    # Clicar no botão da liga
    click_element(driver, LIGA_BUTTOM_STATISTIC_SESSION)

    # Selecionar a liga
    click_element(driver, LIGA_SELECAO_STATISTIC_SESSION)
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


def main():
    """Fluxo principal do script."""
    driver = setup_driver()
    team_stats = TeamStats()

    try:
        teams = {"Real Madrid": REAL_MADRID_XPATH}
        team_name = "Real Madrid"

        # Navegar para a página do time
        navigate_to_team_page(driver, team_name, teams)

        # Extrair estatísticas do time
        extract_team_stats(driver, team_stats)

        # Exibir as estatísticas coletadas
        team_stats.display_stats()

    finally:
        # Fechar o navegador
        driver.quit()


if __name__ == "__main__":
    main()