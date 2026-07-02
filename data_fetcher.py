import pandas as pd
import streamlit as st
import yfinance as yf


@st.cache_data(ttl=3600, show_spinner="Baixando cotações da B3...")
def baixar_dados(tickers: list[str], data_inicio, data_fim) -> pd.DataFrame:
    return yf.download(
        tickers,
        start=data_inicio,
        end=data_fim,
        auto_adjust=True,
        progress=False,
    )


def extrair_fechamento(dados: pd.DataFrame, tickers: list[str]) -> pd.DataFrame:
    if dados.empty:
        return pd.DataFrame()

    fechamento = dados["Close"]
    if isinstance(fechamento, pd.Series):
        fechamento = fechamento.to_frame(name=tickers[0])

    return fechamento.dropna(how="all")


def extrair_volume(dados: pd.DataFrame, tickers: list[str]) -> pd.DataFrame:
    if dados.empty:
        return pd.DataFrame()

    volume = dados["Volume"]
    if isinstance(volume, pd.Series):
        volume = volume.to_frame(name=tickers[0])

    return volume.dropna(how="all")
