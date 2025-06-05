import pandas as pd
import random
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def extrair_features(df):
    df["par"] = df["number"].apply(lambda x: x % 2 == 0)
    df["baixo"] = df["number"].apply(lambda x: x <= 18)
    df["intervalo"] = pd.cut(df["number"], bins=[-1, 12, 24, 36], labels=[0, 1, 2])
    df["soma_lucky"] = df["lucky_numbers"].apply(lambda x: sum(map(int, x.split("-"))) if x else 0)
    return df

def prever_proximos_numeros(history, qtd=10):
    try:
        df = pd.read_csv("resultados.csv")
        df = df.dropna()
        df["lucky_numbers"] = df["lucky_numbers"].fillna("").astype(str)
        df["number"] = df["number"].astype(int)
        df = extrair_features(df)

        X = df[["par", "baixo", "intervalo", "soma_lucky"]]
        y = df["number"]

        model = RandomForestClassifier(n_estimators=150, random_state=42)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model.fit(X_train, y_train)

        # Geração de previsões artificiais baseadas em combinações de features
        previsoes = []
        for _ in range(qtd * 3):  # Gera mais e filtra depois
            amostra = {
                "par": random.choice([True, False]),
                "baixo": random.choice([True, False]),
                "intervalo": random.choice([0, 1, 2]),
                "soma_lucky": random.randint(0, 300)
            }
            X_novo = pd.DataFrame([amostra])
            numero_predito = int(model.predict(X_novo)[0])
            cor = "Vermelho" if numero_predito % 2 == 1 else "Preto"
            linha = (numero_predito - 1) // 3 + 1
            coluna = (numero_predito - 1) % 3 + 1
            faixa = "Baixo" if numero_predito <= 18 else "Alto"

            if 0 <= numero_predito <= 36 and all(n["numero"] != numero_predito for n in previsoes):
                previsoes.append({
                    "numero": numero_predito,
                    "cor": cor,
                    "coluna": coluna,
                    "linha": linha,
                    "range": faixa
                })
            if len(previsoes) >= qtd:
                break

        return previsoes
    except Exception as e:
        print(f"Erro na previsão: {e}")
        return []
