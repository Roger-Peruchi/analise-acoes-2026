# Análise de Ações 2026 — Petrobras, Itaú e Vale

Site em Python (Streamlit) para acompanhar e comparar a performance de PETR4, ITUB4 e VALE3 durante 2026, com dados obtidos do Yahoo Finance via `yfinance`.

## Como rodar

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

O navegador abrirá automaticamente em `http://localhost:8501`.

## Funcionalidades

- Filtro de período dentro de 2026
- Gráfico de preço de fechamento das 3 ações
- Gráfico de performance comparada (base 100), para comparar ativos com preços em escalas diferentes
- Gráfico de volume negociado
- Tabela com retorno total, retorno médio diário, volatilidade, máxima e mínima no período
