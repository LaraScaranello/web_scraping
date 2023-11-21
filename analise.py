import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import csv

nltk.download('vader_lexicon')

favor = 0
contra = 0
neutro = 0

def analisar_sentimento(tweet):
    global favor, contra, neutro
    sia = SentimentIntensityAnalyzer()
    pontuacao = sia.polarity_scores(tweet)
    
    # Determinar a polaridade com base na pontuação do VADER
    if pontuacao['compound'] >= -0.00:
        print(pontuacao['compound'])
        favor = favor + 1
        return "A favor"
    elif pontuacao['compound'] <= -0.5:
        print(pontuacao['compound'])
        contra = contra + 1
        return "Contra"
    elif -0.5 <= pontuacao['compound'] <= 0.0:
        print(pontuacao['compound'])
        neutro = neutro + 1
        return "Neutro"

with open('tweets_2021.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        tweet = row[0] 
        sentimento = analisar_sentimento(tweet)
        print(f"Tweet: {tweet}")
        print(f"Sentimento: {sentimento}")
        print(f"A favor: {favor}")
        print(f"contra: {contra}")
        print(f"Neutro: {neutro}")
        print()

with open('tweets_2022.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        tweet = row[0] 
        sentimento = analisar_sentimento(tweet)
        print(f"Tweet: {tweet}")
        print(f"Sentimento: {sentimento}")
        print(f"A favor: {favor}")
        print(f"contra: {contra}")
        print(f"Neutro: {neutro}")
        print()

with open('tweets_2023.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        tweet = row[0] 
        sentimento = analisar_sentimento(tweet)
        print(f"Tweet: {tweet}")
        print(f"Sentimento: {sentimento}")
        print(f"A favor: {favor}")
        print(f"contra: {contra}")
        print(f"Neutro: {neutro}")
        print()