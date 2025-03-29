from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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