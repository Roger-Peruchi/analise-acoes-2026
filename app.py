from datetime import date

import plotly.express as px

import streamlit as st

from analysis import calcular_estatisticas, calcular_retorno_normalizado
from data_fetcher import baixar_dados, extrair_fechamento, extrair_volume

ATIVOS = {
    "PETR4.SA": "Petrobras",
    "ITUB4.SA": "Itaú",
    "VALE3.SA": "Vale",
}

st.set_page_config(page_title="Análise de Ações 2026", layout="wide")
st.title("Análise de Ações — Petrobras, Itaú e Vale (2026)")

col1, col2 = st.columns(2)
data_inicio = col1.date_input(
    "Data inicial", value=date(2026, 1, 1), min_value=date(2026, 1, 1), max_value=date.today()
)
data_fim = col2.date_input(
    "Data final", value=date.today(), min_value=date(2026, 1, 1), max_value=date.today()
)

if data_inicio >= data_fim:
    st.error("A data inicial precisa ser anterior à data final.")
    st.stop()

tickers = list(ATIVOS.keys())
dados_brutos = baixar_dados(tickers, data_inicio, data_fim)

if dados_brutos.empty:
    st.warning("Não foi possível obter cotações para o período selecionado. Tente outro intervalo de datas.")
    st.stop()

fechamento = extrair_fechamento(dados_brutos, tickers).rename(columns=ATIVOS)
volume = extrair_volume(dados_brutos, tickers).rename(columns=ATIVOS)

if fechamento.empty:
    st.warning("Não há dados de fechamento disponíveis para o período selecionado.")
    st.stop()

st.subheader("Preço de fechamento (R$)")
fig_precos = px.line(fechamento, labels={"value": "Preço (R$)", "Date": "Data", "variable": "Ação"})
st.plotly_chart(fig_precos, use_container_width=True)

st.subheader("Performance comparada (base 100)")
retorno_normalizado = calcular_retorno_normalizado(fechamento)
fig_performance = px.line(
    retorno_normalizado, labels={"value": "Índice (base 100)", "Date": "Data", "variable": "Ação"}
)
st.plotly_chart(fig_performance, use_container_width=True)

st.subheader("Volume negociado")
fig_volume = px.bar(volume, labels={"value": "Volume", "Date": "Data", "variable": "Ação"}, barmode="group")
st.plotly_chart(fig_volume, use_container_width=True)

st.subheader("Resumo estatístico")
st.dataframe(calcular_estatisticas(fechamento), use_container_width=True)
