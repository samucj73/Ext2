import streamlit as st
from data_handler import fetch_latest_result, salvar_resultado_em_arquivo
from modelo_ia import prever_proximos_numeros_com_ia
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import os

st.set_page_config(page_title="Monitor XXXtreme", layout="centered")
st.markdown("<h1 style='text-align:center;'>🎰 Monitor de Sorteios - XXXtreme Lightning Roulette</h1>", unsafe_allow_html=True)

# Auto refresh a cada 10 segundos
st_autorefresh(interval=10_000, key="refresh")

# Estado da sessão
if "history" not in st.session_state:
    st.session_state.history = []
if "last_seen_timestamp" not in st.session_state:
    st.session_state.last_seen_timestamp = None
if "ultima_previsao" not in st.session_state:
    st.session_state.ultima_previsao = None

# Recuperar histórico do CSV, se vazio
if not st.session_state.history:
    if os.path.exists("resultados.csv"):
        df_hist = pd.read_csv("resultados.csv").dropna()
        historico_recuperado = df_hist.iloc[-50:][::-1].to_dict("records")
        st.session_state.history = historico_recuperado
        if historico_recuperado:
            st.session_state.last_seen_timestamp = historico_recuperado[0]["timestamp"]

# Captura novo sorteio
result = fetch_latest_result()
if result and result["timestamp"] != st.session_state.last_seen_timestamp:
    st.session_state.history.insert(0, result)
    st.session_state.history = st.session_state.history[:50]
    st.session_state.last_seen_timestamp = result["timestamp"]
    salvar_resultado_em_arquivo(result)

    # Previsão em tempo real com IA
    previsoes_rapidas = prever_proximos_numeros_com_ia("resultados.csv", qtd=1)
    if previsoes_rapidas:
        st.session_state.ultima_previsao = previsoes_rapidas[0]

# TABS
abas = st.tabs(["📡 Monitoramento", "📈 Análise", "🔮 Previsões Futuras"])

# 📡 Aba 1 – Monitoramento
with abas[0]:
    st.subheader("🎲 Números Sorteados ao Vivo")

    if st.session_state.history:
        for item in st.session_state.history[:10]:
            st.write(f"🎯 Número: {item['number']} | ⚡ Lucky: {item['lucky_numbers']} | 🕒 {item['timestamp']}")
    else:
        st.info("⏳ Aguardando os primeiros números...")

    st.markdown(f"📊 Números coletados: **{len(st.session_state.history)}** / 50")

    if st.session_state.ultima_previsao:
        st.markdown("---")
        st.subheader("🔮 Próximo Número Previsto (IA em tempo real):")
        prev = st.session_state.ultima_previsao
        st.markdown(
            f"🎯 **Número:** `{prev['numero']}` | 🎨 Cor: `{prev['cor']}` | 📊 Coluna: `{prev['coluna']}` | 🧱 Linha: `{prev['linha']}`"
            f" | ⬆⬇ Tipo: `{prev['range']}` | 🔚 Terminal: `{prev['terminal']}`"
        )

# 📈 Aba 2 – Análise
with abas[1]:
    st.subheader("📊 Estatísticas dos Últimos Sorteios")

    if len(st.session_state.history) >= 10:
        if st.button("🔍 Analisar"):
            numeros = [int(item["number"]) for item in st.session_state.history]
            freq = {n: numeros.count(n) for n in set(numeros)}
            top_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:10]

            st.write("🎯 **Top 10 Números Mais Frequentes:**")
            for n, f in top_freq:
                st.write(f"➡️ Número {n} saiu {f} vezes")
    else:
        st.info("📉 É necessário pelo menos 10 sorteios para análise.")

# 🔮 Aba 3 – Previsões Futuras
with abas[2]:
    st.subheader("🔮 Previsão dos Próximos Números (IA)")

    previsoes = prever_proximos_numeros_com_ia("resultados.csv", qtd=10)

    if previsoes:
        numeros_sorteados = [int(item["number"]) for item in st.session_state.history[:1]]

        for i, item in enumerate(previsoes, 1):
            texto = (
                f"**#{i}** 🎯 Número: `{item['numero']}` | 🎨 Cor: `{item['cor']}`"
                f" | 📊 Coluna: `{item['coluna']}` | 🧱 Linha: `{item['linha']}`"
                f" | ⬆⬇ Tipo: `{item['range']}` | 🔚 Terminal: `{item['terminal']}`"
                f" | ◀️ Vizinho Anterior: `{item['vizinho_anterior']}` | ▶️ Vizinho Posterior: `{item['vizinho_posterior']}`"
            )
            if item['numero'] in numeros_sorteados:
                st.success(texto)
            else:
                st.markdown(texto)
    else:
        st.info("🔄 Aguarde mais dados (mínimo 30 sorteios) para previsão com IA.")

# Rodapé
st.markdown("<hr><p style='text-align:center'>© 2025 - Projeto de Previsão de Roleta com IA</p>", unsafe_allow_html=True)
