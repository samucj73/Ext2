from collections import Counter
import random
import streamlit as st

def analisar_estatisticas(history):
    numeros = [entry["number"] for entry in history if entry["number"] is not None]

    if not numeros:
        st.warning("Nenhum número válido para análise.")
        return

    st.markdown("### 📊 Estatísticas Detalhadas dos Últimos 10 Sorteios")

    # 🔥 Frequência
    freq = Counter(numeros)
    hot = freq.most_common(5)
    cold = freq.most_common()[-5:]

    st.write("🔥 **Números Quentes:**")
    for n, f in hot:
        st.write(f"➡️ Número {n} apareceu {f}x")

    st.write("❄️ **Números Frios:**")
    for n, f in cold:
        st.write(f"➡️ Número {n} apareceu {f}x")

    # 🎨 Cores
    cor_map = {
        1: "vermelho", 3: "vermelho", 5: "vermelho", 7: "vermelho", 9: "vermelho", 12: "vermelho",
        14: "vermelho", 16: "vermelho", 18: "vermelho", 19: "vermelho", 21: "vermelho", 23: "vermelho",
        25: "vermelho", 27: "vermelho", 30: "vermelho", 32: "vermelho", 34: "vermelho", 36: "vermelho"
    }

    vermelho = [n for n in numeros if cor_map.get(n) == "vermelho"]
    preto = [n for n in numeros if n != 0 and n not in cor_map]

    st.write(f"🔴 Vermelhos: {len(vermelho)} | ⚫ Pretos: {len(preto)} | 🟢 Zeros: {numeros.count(0)}")

    # 🔢 Altos / Baixos
    baixos = [n for n in numeros if 1 <= n <= 18]
    altos = [n for n in numeros if 19 <= n <= 36]
    st.write(f"🔽 Baixos (1–18): {len(baixos)} | 🔼 Altos (19–36): {len(altos)}")

    # 📊 Colunas
    colunas = {
        "Coluna 1": [1,4,7,10,13,16,19,22,25,28,31,34],
        "Coluna 2": [2,5,8,11,14,17,20,23,26,29,32,35],
        "Coluna 3": [3,6,9,12,15,18,21,24,27,30,33,36]
    }

    col_counts = {col: len([n for n in numeros if n in nums]) for col, nums in colunas.items()}
    st.write("📊 Distribuição por Colunas:")
    for col, count in col_counts.items():
        st.write(f"{col}: {count}")

    # 📏 Linhas (faixas)
    linhas = {
        "1–12": range(1,13),
        "13–24": range(13,25),
        "25–36": range(25,37)
    }
    lin_counts = {label: len([n for n in numeros if n in r]) for label, r in linhas.items()}
    st.write("📏 Distribuição por Linhas:")
    for label, count in lin_counts.items():
        st.write(f"{label}: {count}")

    # 🎯 Previsão dos 10 próximos números (base simples)
    st.markdown("### 🔮 **Previsão dos Próximos 10 Números**")
    provaveis = [n for n, _ in hot[:3]]  # 3 mais frequentes
    provaveis += random.sample(range(1, 37), 7)  # completa com aleatórios diferentes

    previsao = list(dict.fromkeys(provaveis))[:10]  # remove duplicatas
    st.success(f"🎯 Números Prováveis: {', '.join(map(str, previsao))}")
