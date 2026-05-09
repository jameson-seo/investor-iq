# InvestorIQ 📈
A financial dashboard for Canadian and US markets built with Python and Streamlit. Pull live stock data, analyze performance, compare investments, and simulate portfolio returns in a clean, interactive web interface.

---

## Features

**Stock Lookup**
- Search any TSX or NYSE ticker for 1-year performance data
- View current price, 1-year return, 52-week high/low
- Interactive price chart with optional 50-day moving average overlay
- Market overview on load showing top and lowest performers across 25+ stocks

**Compare Stocks**
- Side-by-side comparison of any two stocks
- Start price, current price, and 1-year return for each
- Investment simulator: enter a dollar amount and see what it would be worth today
- Combined chart showing portfolio value over time

**Portfolio Simulator**
- Build a custom portfolio with any number of stocks and share counts
- Live table showing start value, current value, and return per stock
- Total row summarizing the full portfolio
- Add and remove stocks individually

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Streamlit | Web app framework |
| yfinance | Live market data via Yahoo Finance |
| Plotly | Interactive charts |
| pandas | Data manipulation |

---

## Project Structure

```
investor-iq/
├── app.py          # App config, CSS, sidebar, page routing
├── lookup.py       # Stock Lookup page
├── compare.py      # Compare Stocks page
├── portfolio.py    # Portfolio Simulator page
└── utils.py        # Shared helper functions
```

---

## Getting Started

**1. Clone the repo**
```bash
git clone https://github.com/jameson-seo/investor-iq.git
cd investor-iq
```

**2. Install dependencies**
```bash
pip install streamlit yfinance plotly pandas
```

**3. Run the app**
```bash
python -m streamlit run app.py
```

---

## Supported Markets

Works with any ticker available on Yahoo Finance including:

| Exchange | Example Tickers |
|----------|----------------|
| NYSE / NASDAQ | AAPL, MSFT, NVDA, GOOGL, TSLA, JPM |
| TSX (Canadian) | RY.TO, TD.TO, SHOP.TO, ENB.TO, SU.TO |
| ETFs | SPY, QQQ, XIU.TO |

Any valid Yahoo Finance ticker will work, not limited to the examples above.

---

## Data

All market data is sourced from Yahoo Finance via the yfinance library. Prices are delayed approximately 15 minutes. Data is cached for 1 hour on the market overview page to reduce API calls.

---

*Built as a personal project to explore financial data analysis and interactive dashboard development.*
