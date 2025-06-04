import streamlit as st
from data_handler import fetch_latest_result
from predictor import prever_proximos_numeros  # <- Import do preditor
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Monitor XXXtreme", layout="centered")
st.markdown("<h1 style='text-align:center;'>🎰 Monitor de Sorteios - XXXtreme Lightning Roulette</h1>", unsafe_allow_html=True)

# Auto refresh
st_autorefresh(interval=10_000, key="refresh")

# Estado da sessão
if "history" not in st.session_state:
    st.session_state.history = []
if "last_seen_timestamp" not in st.session_state:
    st.session_state.last_seen_timestamp = None

# Captura novo sorteio
result = fetch_latest_result()
if result and result["timestamp"] != st.session_state.last_seen_timestamp:
    st.session_state.history.insert(0, result)
    st.session_state.history = st.session_state.history[:50]
    st.session_state.last_seen_timestamp = result["timestamp"]

# --- TABS ---
abas = st.tabs(["📡 Monitoramento", "📈 Análise", "🔮 Previsões Futuras"])

# 🟠 Aba 1 – Monitoramento
with abas[0]:
    st.subheader("🎲 Números Sorteados ao Vivo")
    if st.session_state.history:
        for item in st.session_state.history[:10]:
            st.write(f"🎯 Número: {item['number']} | ⚡ Lucky: {item['lucky_numbers']} | 🕒 {item['timestamp']}")
    else:
        st.info("⏳ Aguardando os primeiros números...")

    st.markdown(f"📊 Números coletados: **{len(st.session_state.history)}** / 50")

# 🟡 Aba 2 – Análise
with abas[1]:
    st.subheader("📊 Estatísticas dos Últimos Sorteios")
    if len(st.session_state.history) >= 10:
        if st.button("🔍 Analisar"):
            numeros = [item["number"] for item in st.session_state.history]
            freq = {n: numeros.count(n) for n in set(numeros)}
            top_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:10]

            st.write("🎯 **Top 10 Números Mais Frequentes**:")
            for n, f in top_freq:
                st.write(f"➡️ Número {n} saiu {f} vezes")

# 🟢 Aba 3 – Previsões Futuras
with abas[2]:
    st.subheader("🔮 Previsão dos Próximos Números (IA)")

    previsoes = prever_proximos_numeros(st.session_state.history, qtd=10)

    if previsoes:
        for i, item in enumerate(previsoes, 1):
            st.markdown(f"**#{i}** 🎯 Número: `{item['numero']}` | 🎨 Cor: `{item['cor']}` | 📊 Coluna: `{item['coluna']}` | 🧱 Linha: `{item['linha']}` | ⬆⬇ Tipo: `{item['range']}`")
    else:
        st.info("🔄 Aguarde mais dados (mínimo 20 sorteios) para previsão com IA.")

# Rodapé padrão
st.markdown("<hr><p style='text-align:center'>© 2025 - Projeto de Previsão de Roleta com IA</p>", unsafe_allow_html=True)
