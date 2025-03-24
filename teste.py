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

def extract_position_and_score_stats(driver, position_all_xpath_base, category):
    stats = {}
    try:
        value = driver.find_element(By.XPATH, position_all_xpath_base).text
        key = "classificacao"
        stats[key] = value
        print(stats)

        for key, value in stats.items():
            print(f"{key}: {value}")
        print(f"EXTRAÇÃO {category} DEU CERTO")
    except Exception as e:
        print(f"Erro ao encontrar o elemento: {e}")
        driver.save_screenshot('error_screenshot.png')
    return stats

stats_score = {}
position_all_xpath_base = '/html/body/div[1]/main/div[2]/div/div[2]/div[2]/div[3]/div[2]/div[2]/div/div[1]/span'
#score_league_xpath = f'/html/body/div[1]/main/div[2]/div/div[2]/div[2]/div[3]/div[2]/div[2]/div/div[2]/span/div/span'
extract_position_and_score_stats(driver, position_all_xpath_base, "Score/Posi")



time.sleep(2)

# Uso da função para extrair estatísticas de ataque
resume_xpath_base = '/html/body/div[1]/main/div[2]/div/div[2]/div[2]/div[3]/div[2]/div[3]/div/div/div/div'
extract_stats(driver, resume_xpath_base, 4, "Resumo")

time.sleep(2)


# Esperar até que o novo elemento com o XPath fornecido esteja clicável e clicar nele
attack_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[2]/div/div[2]/div[2]/div[3]/div[2]/div[4]/div/button'))
)
attack_button.click()


# Uso da função para extrair estatísticas de ataque
attack_xpath_base = '/html/body/div[1]/main/div[2]/div/div[2]/div[2]/div[3]/div[2]/div[4]/div/div/div/div'

extract_stats(driver, attack_xpath_base, 19, "Ataque")

time.sleep(2)

# Esperar até que o novo elemento com o XPath fornecido esteja clicável e clicar nele
pass_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[2]/div/div[2]/div[2]/div[3]/div[2]/div[5]/div/button'))
)
pass_button.click()

time.sleep(2)

# Uso da função para extrair estatísticas de passe
pass_xpath_base = '/html/body/div[1]/main/div[2]/div/div[2]/div[2]/div[3]/div[2]/div[5]/div/div/div/div'
extract_stats(driver, pass_xpath_base, 6, "Passe")


time.sleep(5)
# Esperar que o dropdown carregue
time.sleep(2)

# Fechar o navegador
driver.quit()