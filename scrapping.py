from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import pandas as pd
import time

# Configurar o driver
driver = webdriver.Chrome()

# Maximizar a janela do navegador
driver.maximize_window()

# Dicionário com o nome do time e sua URL correspondente
teams = {
    "Real Madrid": "https://www.sofascore.com/pt/time/futebol/real-madrid/2829"
}

# Nome do time que queremos acessar
team_name = "Real Madrid"
url = teams[team_name]

# Acessar a página do time diretamente
driver.get(url)

# Esperar que a página carregue completamente
time.sleep(5)

# Esperar até que o elemento com o XPath fornecido esteja clicável e clicar nele
league_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div[3]/div[2]/div[1]/div/div[1]/button'))
)
league_button.click()

time.sleep(2)

# Esperar até que o novo elemento com o XPath fornecido esteja clicável e clicar nele
league_select = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div[3]/div[2]/div[1]/div/div[1]/div/div/div[1]/div/ul/li[4]/div/div'))
)
league_select.click()

# Esperar que o dropdown carregue
time.sleep(2)

# Esperar até que o novo elemento com o XPath fornecido esteja clicável e clicar nele
attack_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[2]/div/div[2]/div[2]/div[3]/div[2]/div[4]/div/button'))
)
attack_button.click()

time.sleep(2)

stats = {}
try:
    stats_attack_element = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div/div[2]/div[2]/div[3]/div[2]/div[4]/div/div/div/div')
    # Extrair as informações desejadas
    for i in range(1, 20):        
        key_xpath = f'/html/body/div[1]/main/div[2]/div/div[2]/div[2]/div[3]/div[2]/div[4]/div/div/div/div/div[{i}]/span[1]'
        value_xpath = f'/html/body/div[1]/main/div[2]/div/div[2]/div[2]/div[3]/div[2]/div[4]/div/div/div/div/div[{i}]/span[2]'
        key = stats_attack_element.find_element(By.XPATH, key_xpath).text
        value = stats_attack_element.find_element(By.XPATH, value_xpath).text
        stats[key] = value

    # Imprimir as informações extraídas
    for key, value in stats.items():
        print(f"{key}: {value}")
    print("DEU CERTO")
except:
    print(f"Erro ao encontrar o elemento: {e}")
    driver.save_screenshot('error_screenshot.png')


time.sleep(5)
# Esperar que o dropdown carregue
time.sleep(2)

# Fechar o navegador
driver.quit()