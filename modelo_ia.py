# modelo_ia.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

def extrair_caracteristicas(numero):
    return {
        "numero": numero,
        "cor": "vermelho" if numero % 2 == 1 else "preto",
        "coluna": (numero - 1) % 3 + 1,
        "linha": (numero - 1) // 3 + 1,
        "range": "baixo" if numero <= 18 else "alto",
        "terminal": numero % 10,
    }

def preparar_dados(dados):
    X, y = [], []
    for i in range(len(dados) - 5):
        entrada = dados[i:i+5]
        alvo = dados[i+5]
        features = {
            f"n{j+1}": entrada[j] for j in range(5)
        }
        X.append(features)
        y.append(alvo)
    return pd.DataFrame(X), y

def treinar_modelo(X, y):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

def prever_proximos_numeros_com_ia(caminho_csv="resultados.csv", qtd=10):
    try:
        df = pd.read_csv(caminho_csv)
        numeros = df["number"].dropna().astype(int).tolist()

        if len(numeros) < 30:
            return []

        X, y = preparar_dados(numeros)
        model = treinar_modelo(X, y)

        ultimos = numeros[-5:]
        entrada = pd.DataFrame([{
            f"n{j+1}": ultimos[j] for j in range(5)
        }])

        # Probabilidades previstas
        probas = model.predict_proba(entrada)[0]
        classes = model.classes_

        top_indices = np.argsort(probas)[-qtd:][::-1]
        previsoes = []

        for i in top_indices:
            n = classes[i]
            feat = extrair_caracteristicas(n)
            previsoes.append({
                "numero": int(n),
                "cor": feat["cor"],
                "coluna": feat["coluna"],
                "linha": feat["linha"],
                "range": feat["range"],
                "terminal": feat["terminal"],
                "vizinho_anterior": int(n) - 1 if n > 0 else 36,
                "vizinho_posterior": int(n) + 1 if n < 36 else 0,
            })

        return previsoes

    except Exception as e:
        print("Erro na previsão com IA:", e)
        return []
