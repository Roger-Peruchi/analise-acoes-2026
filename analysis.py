import pandas as pd


def calcular_retorno_normalizado(precos: pd.DataFrame) -> pd.DataFrame:
    precos_validos = precos.dropna(how="all")
    primeira_linha_valida = precos_validos.bfill().iloc[0]
    return precos_validos.div(primeira_linha_valida).mul(100)


def calcular_estatisticas(precos: pd.DataFrame) -> pd.DataFrame:
    retornos_diarios = precos.pct_change()
    preco_inicial = precos.bfill().iloc[0]
    preco_atual = precos.ffill().iloc[-1]

    estatisticas = pd.DataFrame({
        "Preço inicial (R$)": preco_inicial,
        "Preço atual (R$)": preco_atual,
        "Retorno no período (%)": (preco_atual / preco_inicial - 1) * 100,
        "Retorno médio diário (%)": retornos_diarios.mean() * 100,
        "Volatilidade diária (%)": retornos_diarios.std() * 100,
        "Máxima (R$)": precos.max(),
        "Mínima (R$)": precos.min(),
    })

    return estatisticas.round(2)
