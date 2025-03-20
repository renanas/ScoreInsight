from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurar o driver
driver = webdriver.Chrome()
driver.get("https://www.sofascore.com/")

# Esperar até que um elemento específico apareça
try:
    elemento = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "event-list-event"))
    )
    print("Elemento encontrado:", elemento.text)
except:
    print("Tempo limite atingido, elemento não encontrado.")

driver.quit()