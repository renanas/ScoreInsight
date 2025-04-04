import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from extractors.coach.coach_actual_club_extractor import extract_performance_stats_actual_club
from extractors.coach.coach_career_info_extractor import extract_coach_stats

def extract_coach(driver, teams, team_name):
    """
    Clica no elemento do técnico na página do clube para acessar a pagina pessoal do técnico.
    """
    try:
        # Localizar o elemento pelo XPath
        time.sleep(2)  # Esperar o carregamento da página        
        
        # Localizar o elemento do link do técnico pelo XPath
        coach_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Treinador']/following-sibling::div/a"))
        )
        coach_element.click()
        time.sleep(2)

        extract_coach_stats(driver)

        extract_performance_stats_actual_club(driver, teams, team_name)

        print("Elemento do técnico clicado com sucesso!")
    except Exception as e:
        print(f"Erro ao clicar no elemento do técnico: {e}")
