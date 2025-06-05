import pandas as pd
import random
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Tabela completa da roleta europeia com propriedades reais
tabela_numeros = {
    0:  {"cor_real": "Verde",    "coluna": 0, "linha": 0,  "terminal": 0, "vizinhos": [26, 32]},
    1:  {"cor_real": "Vermelho", "coluna": 1, "linha": 1,  "terminal": 1, "vizinhos": [33, 20]},
    2:  {"cor_real": "Preto",    "coluna": 2, "linha": 1,  "terminal": 2, "vizinhos": [21, 25]},
    3:  {"cor_real": "Vermelho", "coluna": 3, "linha": 1,  "terminal": 3, "vizinhos": [35, 26]},
    4:  {"cor_real": "Preto",    "coluna": 1, "linha": 2,  "terminal": 4, "vizinhos": [19, 21]},
    5:  {"cor_real": "Vermelho", "coluna": 2, "linha": 2,  "terminal": 5, "vizinhos": [10, 24]},
    6:  {"cor_real": "Preto",    "coluna": 3, "linha": 2,  "terminal": 6, "vizinhos": [34, 27]},
    7:  {"cor_real": "Vermelho", "coluna": 1, "linha": 3,  "terminal": 7, "vizinhos": [28, 29]},
    8:  {"cor_real": "Preto",    "coluna": 2, "linha": 3,  "terminal": 8, "vizinhos": [30, 23]},
    9:  {"cor_real": "Vermelho", "coluna": 3, "linha": 3,  "terminal": 9, "vizinhos": [31, 22]},
    10: {"cor_real": "Preto",    "coluna": 1, "linha": 4,  "terminal": 0, "vizinhos": [5, 23]},
    11: {"cor_real": "Preto",    "coluna": 2, "linha": 4,  "terminal": 1, "vizinhos": [36, 30]},
    12: {"cor_real": "Vermelho", "coluna": 3, "linha": 4,  "terminal": 2, "vizinhos": [28, 35]},
    13: {"cor_real": "Preto",    "coluna": 1, "linha": 5,  "terminal": 3, "vizinhos": [27, 36]},
    14: {"cor_real": "Vermelho", "coluna": 2, "linha": 5,  "terminal": 4, "vizinhos": [31, 20]},
    15: {"cor_real": "Preto",    "coluna": 3, "linha": 5,  "terminal": 5, "vizinhos": [19, 32]},
    16: {"cor_real": "Vermelho", "coluna": 1, "linha": 6,  "terminal": 6, "vizinhos": [33, 24]},
    17: {"cor_real": "Preto",    "coluna": 2, "linha": 6,  "terminal": 7, "vizinhos": [25, 34]},
    18: {"cor_real": "Vermelho", "coluna": 3, "linha": 6,  "terminal": 8, "vizinhos": [22, 29]},
    19: {"cor_real": "Vermelho", "coluna": 1, "linha": 7,  "terminal": 9, "vizinhos": [4, 15]},
    20: {"cor_real": "Preto",    "coluna": 2, "linha": 7,  "terminal": 0, "vizinhos": [1, 14]},
    21: {"cor_real": "Vermelho", "coluna": 3, "linha": 7,  "terminal": 1, "vizinhos": [2, 4]},
    22: {"cor_real": "Preto",    "coluna": 1, "linha": 8,  "terminal": 2, "vizinhos": [18, 9]},
    23: {"cor_real": "Vermelho", "coluna": 2, "linha": 8,  "terminal": 3, "vizinhos": [8, 10]},
    24: {"cor_real": "Preto",    "coluna": 3, "linha": 8,  "terminal": 4, "vizinhos": [5, 16]},
    25: {"cor_real": "Vermelho", "coluna": 1, "linha": 9,  "terminal": 5, "vizinhos": [2, 17]},
    26: {"cor_real": "Preto",    "coluna": 2, "linha": 9,  "terminal": 6, "vizinhos": [0, 3]},
    27: {"cor_real": "Vermelho", "coluna": 3, "linha": 9,  "terminal": 7, "vizinhos": [6, 13]},
    28: {"cor_real": "Preto",    "coluna": 1, "linha": 10, "terminal": 8, "vizinhos": [7, 12]},
    29: {"cor_real": "Vermelho", "coluna": 2, "linha": 10, "terminal": 9, "vizinhos": [7, 18]},
    30: {"cor_real": "Preto",    "coluna": 3, "linha": 10, "terminal": 0, "vizinhos": [8, 11]},
    31: {"cor_real": "Vermelho", "coluna": 1, "linha": 11, "terminal": 1, "vizinhos": [9, 14]},
    32: {"cor_real": "Preto",    "coluna": 2, "linha": 11, "terminal": 2, "vizinhos": [15, 0]},
    33: {"cor_real": "Vermelho", "coluna": 3, "linha": 11, "terminal": 3, "vizinhos": [1, 16]},
    34: {"cor_real": "Vermelho", "coluna": 1, "linha": 12, "terminal": 4, "vizinhos": [6, 17]},
    35: {"cor_real": "Preto",    "coluna": 2, "linha": 12, "terminal": 5, "vizinhos": [3, 12]},
    36: {"cor_real": "Vermelho", "coluna": 3, "linha": 12, "terminal": 6, "vizinhos": [11, 13]},
}

def extrair_features(df):
    df["par"] = df["number"] % 2 == 0
    df["baixo"] = df["number"] <= 18
    df["intervalo"] = pd.cut(df["number"], bins=[-1, 12, 24, 36], labels=[0, 1, 2])
    df["soma_lucky"] = df["lucky_numbers"].apply(lambda x: sum(map(int, x.split("-"))) if x else 0)
    
    df["terminal"] = df["number"] % 10
    df["coluna"] = df["number"].map(lambda x: tabela_numeros.get(x, {}).get("coluna", -1))
    df["linha"] = df["number"].map(lambda x: tabela_numeros.get(x, {}).get("linha", -1))
    df["vizinho_1"] = df["number"].map(lambda x: tabela_numeros.get(x, {}).get("vizinhos", [None, None])[0])
    df["vizinho_2"] = df["number"].map(lambda x: tabela_numeros.get(x, {}).get("vizinhos", [None, None])[1])
    df["cor_real"] = df["number"].map(lambda x: tabela_numeros.get(x, {}).get("cor_real", "Desconhecida"))

    return df

def prever_proximos_numeros(history, qtd=10):
    try:
        df = pd.read_csv("resultados.csv")
        df.dropna(inplace=True)
        df["lucky_numbers"] = df["lucky_numbers"].fillna("").astype(str)
        df["number"] = df["number"].astype(int)
        df = extrair_features(df)

        features = ["par", "baixo", "intervalo", "soma_lucky", "terminal", "coluna", "linha"]
        X = df[features]
        y = df["number"]

        model = RandomForestClassifier(n_estimators=200, random_state=42)
        X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
        model.fit(X_train, y_train)

        previsoes = []
        tentativas = 0
        while len(previsoes) < qtd and tentativas < qtd * 5:
            amostra = {
                "par": random.choice([True, False]),
                "baixo": random.choice([True, False]),
                "intervalo": random.choice([0, 1, 2]),
                "soma_lucky": random.randint(0, 300),
                "terminal": random.randint(0, 9),
                "coluna": random.randint(1, 3),
                "linha": random.randint(1, 12)
            }
            X_novo = pd.DataFrame([amostra])
            numero_predito = int(model.predict(X_novo)[0])

            if 0 <= numero_predito <= 36 and all(n["numero"] != numero_predito for n in previsoes):
                props = tabela_numeros.get(numero_predito, {
                    "cor_real": "Desconhecida", "coluna": "-", "linha": "-", "terminal": "-", "vizinhos": [None, None]
                })
                previsoes.append({
                    "numero": numero_predito,
                    "cor": props["cor_real"],
                    "coluna": props["coluna"],
                    "linha": props["linha"],
                    "range": "Baixo" if numero_predito <= 18 else "Alto",
                    "terminal": numero_predito % 10,
                    "vizinho_1": props["vizinhos"][0],
                    "vizinho_2": props["vizinhos"][1]
                })

            tentativas += 1

        return previsoes

    except Exception as e:
        print(f"Erro na previsão: {e}")
        return []
