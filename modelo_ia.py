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
        features = {}

        for j in range(5):
            f = extrair_caracteristicas(entrada[j])
            for chave, valor in f.items():
                features[f"n{j+1}_{chave}"] = valor

        for j in range(4):
            features[f"dif_{j+1}"] = abs(entrada[j+1] - entrada[j])

        X.append(features)
        y.append(alvo)

    df_X = pd.DataFrame(X)

    # Codificar variáveis categóricas automaticamente
    for col in df_X.select_dtypes(include='object').columns:
        le = LabelEncoder()
        df_X[col] = le.fit_transform(df_X[col])

    return df_X, y

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
        entrada_features = {}

        for j in range(5):
            f = extrair_caracteristicas(ultimos[j])
            for chave, valor in f.items():
                entrada_features[f"n{j+1}_{chave}"] = valor

        for j in range(4):
            entrada_features[f"dif_{j+1}"] = abs(ultimos[j+1] - ultimos[j])

        entrada_df = pd.DataFrame([entrada_features])

        # Codificar categorias da entrada igual ao treinamento
        for col in entrada_df.select_dtypes(include='object').columns:
            le = LabelEncoder()
            entrada_df[col] = le.fit_transform(entrada_df[col])

        # Previsões
        probas = model.predict_proba(entrada_df)[0]
        classes = model.classes_

        top_indices = np.argsort(probas)[-qtd*2:][::-1]
        previsoes = []

        for i in top_indices:
            n = int(classes[i])
            if any(p["numero"] == n for p in previsoes):
                continue
            feat = extrair_caracteristicas(n)
            previsoes.append({
                "numero": n,
                "cor": feat["cor"],
                "coluna": feat["coluna"],
                "linha": feat["linha"],
                "range": feat["range"],
                "terminal": feat["terminal"],
                "vizinho_anterior": n - 1 if n > 0 else 36,
                "vizinho_posterior": n + 1 if n < 36 else 0,
            })
            if len(previsoes) >= qtd:
                break

        return previsoes

    except Exception as e:
        print("Erro na previsão com IA:", e)
        return []
