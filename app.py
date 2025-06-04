
import streamlit as st
import time
from data_handler import fetch_latest_result, salvar_resultado_em_arquivo
from analysis import analisar_estatisticas
from predictor import prever_numeros_provaveis

st.set_page_config(page_title="Monitor XXXtreme", layout="centered")
st.markdown("<h1 style='text-align: center;'>🎰 Monitor de Sorteios - XXXtreme Lightning Roulette</h1>", unsafe_allow_html=True)

# Inicializa estados
if "history" not in st.session_state:
    st.session_state.history = []
if "last_seen_timestamp" not in st.session_state:
    st.session_state.last_seen_timestamp = None

# 🔍 Busca o último resultado
result = fetch_latest_result()

if result and result["timestamp"] != st.session_state.last_seen_timestamp:
    st.session_state.history.insert(0, result)
    st.session_state.last_seen_timestamp = result["timestamp"]
    st.session_state.history = st.session_state.history[:50]

    # Salva a cada 10 sorteios
    if len(st.session_state.history) % 10 == 0:
        salvar_resultado_em_arquivo(st.session_state.history[:10])

# 🎯 Mostra números em tempo real
st.subheader("🎲 Números Sorteados ao Vivo:", divider='rainbow')
if st.session_state.history:
    for item in st.session_state.history[:10]:
        st.write(f"🎯 Número: {item['number']} | ⚡ Lucky: {item['lucky_numbers']} | 🕒 {item['timestamp']}")
else:
    st.info("⏳ Aguardando os primeiros números...")

st.markdown(f"<p style='text-align: center;'>📊 Números coletados: <b>{len(st.session_state.history)}</b> / 50</p>", unsafe_allow_html=True)

# Botão de análise aparece ao atingir 10
if len(st.session_state.history) >= 10:
    st.subheader("📈 Estatísticas dos Últimos 10 Sorteios", divider='rainbow')
    if st.button("🔍 Analisar os 10 últimos sorteios"):
        estatisticas = analisar_estatisticas(st.session_state.history[:10])
        for titulo, valores in estatisticas.items():
            st.markdown(f"**{titulo}**")
            for v in valores:
                st.write("➡️", v)

        # Previsão
        st.subheader("🔮 Previsão de Próximos Números Prováveis", divider='rainbow')
        previsao = prever_numeros_provaveis()
        st.write("➡️", ', '.join(map(str, previsao)))

# Rodapé
st.markdown("---")
st.markdown("<p style='text-align: center;'>Desenvolvido por Kanō • Monitor de Roleta XXXtreme 🎰</p>", unsafe_allow_html=True)
