from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import time
import csv
import os
import codecs
import re

def clean_tweet(tweet_text):
    # Remove URLs
    tweet_text = re.sub(r"http\S+|www\S+|https\S+", '', tweet_text)
    # Remove menções a usuários (@username)
    tweet_text = re.sub(r'@\w+', '', tweet_text)
    # Remove hashtags (#hashtag)
    tweet_text = re.sub(r'#\w+', '', tweet_text)
    return tweet_text

# Configura o driver do Selenium para o Chrome
options = webdriver.ChromeOptions()
options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

# Cria o driver Chrome
driver = webdriver.Chrome(options=options)

# URL para a abertura da página de login do twitter
url1 = 'https://twitter.com/login'

# Abre a página no navegador
driver.get(url1)

# LOGIN
# inserir usuário
sleep(3)
usuario = driver.find_element(By.XPATH, "//input[@name='text']")
usuario.send_keys("@Lara2R167598")
avanca = driver.find_element(By.XPATH, "//span[contains(text(),'Avançar')]")
avanca.click()

# inserir senha
sleep(3)
senha = driver.find_element(By.XPATH, "//input[@name='password']")
senha.send_keys("LSRR@16@09")
entrar = driver.find_element(By.XPATH, "//span[contains(text(),'Entrar')]")
entrar.click()
sleep(3)

# Data de início
data_inicio = datetime(2023, 7, 1)

# Intervalo de 10 dias
intervalo = timedelta(days=10)

# Data de término (10 dias após a data de início)
data_fim = data_inicio + intervalo

# Data final 
data_final_desejada = datetime(2023, 10, 31)

# Diretório onde vai salvar o arquivo CSV
diretorio_destino = r'D:\ADS_FATEC\6_periodo\TG_II'

# Arquivo CSV
nome_arquivo_csv = 'tweets_2023.csv'

# Verifica se o diretório de destino existe
# se não existir, cria
if not os.path.exists(diretorio_destino):
    os.makedirs(diretorio_destino)

# Caminho completo para o arquivo CSV
caminho_arquivo_csv = os.path.join(diretorio_destino, nome_arquivo_csv)

# Verificaa se o arquivo CSV já existe
if os.path.exists(caminho_arquivo_csv):
    modo_arquivo = 'a'  # Modo de adição (append)
else:
    modo_arquivo = 'w'  # Modo de escrita (create)

# Inicializa uma lista para armazenar todos os tweets coletados
lista_total = []
count = 0

while data_inicio < data_final_desejada:
    
    # Constroe a URL com as datas atuais
    url = f'https://twitter.com/search?q=vacina%C3%A7%C3%A3o%20covid%20crian%C3%A7as%20since%3A
    {data_inicio:%Y-%m-%d}%20until%3A{data_fim:%Y-%m-%d}&src=typed_query'

    # Abre a página no navegador
    driver.get(url)

    # Rola a página para baixo para carregar mais tweets 
    for _ in range(20):  # Rolando 5 vezes
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(1) 

    # Espera até que os tweets sejam carregados na página
    print(f"Esperando por elementos ... {data_inicio:%Y-%m-%d}")
    time.sleep(10)

    # Encontra e extrai os tweets
    tweets = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='tweetText']")

    lista = []
    for index, tweet in enumerate(tweets):
        try:
            tweet_text = clean_tweet(tweet.text)     
            lista.append(tweet_text)
        except Exception as e:
            print(f"Erro ao extrair tweet: {e}")

    # Adiciona os tweets coletados nesta rodada à lista total
    lista_total.extend(lista)

    # Avança a data de início e término para o próximo intervalo 
    data_inicio += intervalo
    data_fim += intervalo

# Salva todos os tweets coletados no arquivo CSV 
with codecs.open(caminho_arquivo_csv, modo_arquivo, encoding='utf-8-sig') as csvfile:
    csv_writer = csv.writer(csvfile)
    for tweet in lista_total:
        try:
            # Remove quebras de linha por espaços em branco
            tweet_sem_quebra_de_linha = tweet.replace('\n', ' ')
            # Escreve o tweet no arquivo CSV
            csv_writer.writerow([tweet_sem_quebra_de_linha])
        except Exception as e:
            print(f"Erro ao escrever tweet no arquivo CSV: {e}")

# Fecha o navegador
driver.quit()
