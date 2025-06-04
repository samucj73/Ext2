import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from collections import Counter
import random

# 🔴 Mapeamento de cor para cada número da roleta
def get_color(number):
    if number == 0:
        return "verde"
    vermelhos = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
    return "vermelho" if number in vermelhos else "preto"

# 🔠 Coluna
def get_column(number):
    if number == 0: return 0
    if number % 3 == 1: return 1
    if number % 3 == 2: return 2
    return 3

# 🧱 Linha
def get_line(number):
    if number == 0: return 0
    if number <= 12: return 1
    elif number <= 24: return 2
    return 3

# ⬆⬇ Alto ou baixo
def get_range(number):
    if number == 0: return "zero"
    return "baixo" if number <= 18 else "alto"

# 🔢 Cria DataFrame com features dos números
def preparar_dados_para_treinamento(historico):
    dados = []
    for item in historico:
        n = item["number"]
        if n is None:
            continue
        dados.append({
            "numero": n,
            "cor": get_color(n),
            "coluna": get_column(n),
            "linha": get_line(n),
            "range": get_range(n)
        })
    df = pd.DataFrame(dados)
    
    # Conversão de texto para número
    df['cor'] = df['cor'].map({'vermelho': 1, 'preto': 0, 'verde': 2})
    df['range'] = df['range'].map({'baixo': 0, 'alto': 1, 'zero': 2})
    return df

# 🔮 Função principal de previsão
def prever_proximos_numeros(historico, qtd=10):
    df = preparar_dados_para_treinamento(historico)

    if len(df) < 20:
        return []  # dados insuficientes

    # Entradas e saídas
    X = df.drop(columns=["numero"])
    y = df["numero"]

    # Treina modelo
    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X, y)

    # Gera previsões fictícias usando dados recentes
    ultimos = X.tail(5)
    previsoes = []
    for _ in range(qtd):
        entrada = ultimos.sample(1, replace=True, random_state=random.randint(0,10000))
        pred = modelo.predict(entrada)[0]
        previsoes.append(pred)

    # Remove duplicados mantendo a ordem
    previsoes_unicas = list(dict.fromkeys(previsoes))[:qtd]

    # Extrai atributos
    resultados = []
    for n in previsoes_unicas:
        resultados.append({
            "numero": n,
            "cor": get_color(n),
            "coluna": get_column(n),
            "linha": get_line(n),
            "range": get_range(n)
        })

    return resultados
