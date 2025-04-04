from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
            competition_text = option.find_element(By.XPATH, ".//bdi").text
            if competition_text == competition_name:
                option.click()
                print(f"Competição '{competition_name}' selecionada com sucesso.")
                return

        print(f"Competição '{competition_name}' não encontrada.")
    except Exception as e:
        print(f"Erro ao selecionar a competição: {e}")