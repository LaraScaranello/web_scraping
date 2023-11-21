import os
import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import matplotlib.pyplot as plt
import seaborn as sns

# Verifica se o arquivo 'tweets_classificados.csv' já existe e, se existir, apaga
output_file_path = 'D:/ADS_FATEC/6_periodo/TG_II/tweets_classificados_2023.csv'
if os.path.exists(output_file_path):
    os.remove(output_file_path)

# Carrega os dados do CSV com tweets não classificados
lines = []
file_path = 'D:/ADS_FATEC/6_periodo/TG_II/tweets_2023.csv'

# Abre o arquivo CSV e lê os dados
with open(file_path, 'r', encoding='utf-8-sig') as file:
    for line in file:
        # Adiciona cada linha à lista, removendo qualquer espaço em branco adicional
        lines.append(line.strip())  

# Escolhe o modelo pré-treinado
model_name = "bert-base-uncased"

# Carrega o tokenizador e o modelo
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

# Lista para armazenar os sentimentos classificados
sentiments = []

# Inicializa dicionários para contar os sentimentos
contagem_sentimentos = {'Positivo': 0, 'Negativo': 0}

# Cria uma lista para armazenar os tweets classificados
classified_tweets = []

# Para cada tweet não classificado
for tweet in lines:
    # Tokeniza o texto
    inputs = tokenizer(tweet, return_tensors="pt", padding=True, truncation=True)

    # Realiza a inferência com o modelo
    outputs = model(**inputs)
    logits = outputs.logits

    # Calcula as probabilidades
    probabilities = torch.softmax(logits, dim=1)

    # Obtem o índice da classe com a maior probabilidade
    predicted_class = torch.argmax(probabilities, dim=1).item()

    # Interpreta o resultado
    sentiment_classes = ["Positivo", "Negativo"]
    sentiment = sentiment_classes[predicted_class]

    sentiments.append(sentiment)

    # Atualiza a contagem de acordo com o sentimento
    contagem_sentimentos[sentiment] += 1

    # Salva o tweet classificado com seu sentimento em uma lista
    classified_tweets.append((tweet, sentiment))

# Salva os tweets classificados em um arquivo CSV
classified_data = pd.DataFrame(classified_tweets, columns=['Tweets', 'Sentimento'])
classified_data.to_csv(output_file_path, index=False, encoding='utf-8-sig')

# Mostra o total de positivo e negativo
total_positivo = contagem_sentimentos['Positivo']
total_negativo = contagem_sentimentos['Negativo']

# Calcula as porcentagens
total_tweets = total_positivo + total_negativo
percent_positivo = (total_positivo / total_tweets) * 100
percent_negativo = (total_negativo / total_tweets) * 100

# Cria um gráfico de barras para visualizar a distribuição dos sentimentos
sentiment_labels = ['Positivo', 'Negativo']
sentiment_percentages = [percent_positivo, percent_negativo]

plt.figure(figsize=(6, 4))
sns.barplot(x=sentiment_labels, y=sentiment_percentages)
plt.title('Distribuição de Sentimentos (Porcentagem)')
plt.xlabel('Sentimento')
plt.ylabel('Porcentagem')
plt.ylim(0, 100)
plt.show()