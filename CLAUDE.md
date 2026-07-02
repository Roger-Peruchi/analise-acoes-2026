# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A Streamlit site that downloads, analyzes, and charts the 2026 performance of three B3-listed stocks: Petrobras (PETR4), Itaú (ITUB4), and Vale (VALE3). Data comes from Yahoo Finance via `yfinance`.

## Repository

- GitHub: https://github.com/Roger-Peruchi/analise-acoes-2026 (public)
- Default branch: `main`
- Remote `origin` uses HTTPS; auth is handled by GitHub CLI (`gh auth login`), not a stored credential/token in the repo.

## Commands

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The app opens at `http://localhost:8501`. On Windows, `pip`/`streamlit` are often not on PATH directly — always invoke via `python -m`.

There is no test suite, linter, or build step in this project.

## Architecture

Three-module pipeline wired together in `app.py`:

- **`data_fetcher.py`** — talks to Yahoo Finance. `baixar_dados()` is the only network call and is wrapped in `@st.cache_data(ttl=3600)` so repeated Streamlit reruns (e.g. widget interaction) don't re-hit the API. It returns the raw multi-ticker `yf.download()` DataFrame (multi-index columns: price field × ticker). `extrair_fechamento()` / `extrair_volume()` slice that raw frame into a plain ticker-columns DataFrame, handling the case where `yf.download` collapses to a `Series` when only one ticker has data.
- **`analysis.py`** — pure functions over a fechamento (closing price) DataFrame, no I/O or Streamlit dependency. `calcular_retorno_normalizado()` rebases each ticker's series to 100 at its first valid value, which is what makes tickers with very different price scales (e.g. VALE3 ~R$78 vs PETR4 ~R$38) visually comparable on one chart. `calcular_estatisticas()` produces the summary table (retorno total, retorno médio diário, volatilidade, máx/mín).
- **`app.py`** — the only file with UI/Streamlit-page code. Holds the `ATIVOS` dict (ticker → display name in Portuguese) as the single source of truth for which stocks are tracked; renaming/adding a ticker there is the only change needed to track a different set of stocks. Flow: date inputs → `baixar_dados` → `extrair_fechamento`/`extrair_volume` (renamed via `ATIVOS`) → three Plotly charts (price, normalized performance, volume) → `st.dataframe` stats table. Guards with `st.warning`/`st.stop()` when a date range returns no data.

When adding a new chart or metric, prefer extending `analysis.py` with a pure function over the fechamento DataFrame and calling it from `app.py`, keeping data-fetching, calculation, and presentation separated as they are now.

## Data notes

- Tickers use the `.SA` suffix required by Yahoo Finance for B3-listed stocks.
- The date range is anchored to 2026 (`date(2026, 1, 1)` as the minimum selectable date in `app.py`) since that's the year being analyzed.
- `yfinance` occasionally returns a `Series` instead of a `DataFrame` when data for only one ticker resolves — `extrair_fechamento`/`extrair_volume` already normalize this, don't assume `dados["Close"]` is always 2D.
