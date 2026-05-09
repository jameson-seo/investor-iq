import streamlit as st
import yfinance as yf
import pandas as pd
import lookup, compare, portfolio

st.set_page_config(page_title="Canadian Investor Dashboard", layout="wide", page_icon="📈")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background-color: #0a0e1a; }
.top-bar { background: linear-gradient(90deg, #1a56db, #0ea5e9, #06b6d4); height: 3px; width: 100%; margin-bottom: 2rem; border-radius: 2px; }
[data-testid="stSidebar"] { background-color: #0f1422; border-right: 1px solid #1e2433; }
.sidebar-logo { font-size: 20px; font-weight: 700; color: #ffffff; letter-spacing: -0.5px; padding: 0.5rem 0; }
.sidebar-logo span { color: #0ea5e9; }
.sidebar-sub { font-size: 11px; color: #4b5563; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 1.5rem; }
.sidebar-section { font-size: 10px; font-weight: 600; color: #374151; letter-spacing: 1px; text-transform: uppercase; margin: 1.5rem 0 0.5rem 0; }
.sidebar-divider { border: none; border-top: 1px solid #1e2433; margin: 1rem 0; }
.market-pill { display: flex; align-items: center; gap: 6px; padding: 6px 10px; background: #131929; border: 1px solid #1e2433; border-radius: 8px; margin-bottom: 6px; font-size: 12px; color: #9ca3af; }
.market-pill .ticker { font-weight: 600; color: #e2e8f0; font-size: 12px; }
.market-pill .positive { color: #10b981; }
.market-pill .negative { color: #ef4444; }
.page-title { font-size: 28px; font-weight: 700; color: #f1f5f9; letter-spacing: -0.5px; margin-bottom: 0.25rem; }
.page-subtitle { font-size: 14px; color: #4b5563; margin-bottom: 2rem; }
[data-testid="stMetricValue"] { font-family: 'Inter', sans-serif !important; font-size: 24px !important; font-weight: 700 !important; }
div[data-testid="metric-container"] { background: #0f1422; border: 1px solid #1e2433; border-radius: 12px; padding: 1rem 1.2rem; }
div[data-testid="stAlert"] { background: #0ea5e910; border: 1px solid #0ea5e930; border-radius: 10px; color: #7dd3fc; }
.stButton > button { background: #131929; border: 1px solid #1e2433; color: #e2e8f0; border-radius: 8px; font-family: 'Inter', sans-serif; font-size: 13px; font-weight: 500; transition: all 0.15s ease; }
.stButton > button:hover { background: #1a56db; border-color: #1a56db; color: white; }
input[type="text"] { background: #131929 !important; border: 1px solid #1e2433 !important; border-radius: 8px !important; color: #e2e8f0 !important; font-family: 'Inter', sans-serif !important; }
h1, h2, h3 { font-family: 'Inter', sans-serif !important; font-weight: 600 !important; letter-spacing: -0.3px; color: #f1f5f9 !important; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="sidebar-logo">Investor<span>IQ</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Canadian & US Markets</div>', unsafe_allow_html=True)
    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section">Navigation</div>', unsafe_allow_html=True)

    if "page" not in st.session_state:
        st.session_state.page = "Stock Lookup"

    pages = {"Stock Lookup": "Search any stock", "Compare Stocks": "Side by side analysis", "Portfolio Simulator": "Simulate your returns"}
    for p, desc in pages.items():
        if st.button(p, key=p, use_container_width=True):
            st.session_state.page = p

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section">Watchlist</div>', unsafe_allow_html=True)

    watchlist = [("SPY", "S&P 500"), ("QQQ", "Nasdaq"), ("XIU.TO", "TSX 60")]
    for ticker, name in watchlist:
        data = yf.download(ticker, period="5d", auto_adjust=True, progress=False)
        if not data.empty:
            close = data["Close"].iloc[:, 0] if isinstance(data["Close"], pd.DataFrame) else data["Close"]
            change = ((float(close.iloc[-1]) - float(close.iloc[-2])) / float(close.iloc[-2])) * 100
            color = "positive" if change >= 0 else "negative"
            arrow = "▲" if change >= 0 else "▼"
            st.markdown(f'<div class="market-pill"><span class="ticker">{ticker}</span><span style="color:#4b5563; font-size:11px;">{name}</span><span class="{color}" style="margin-left:auto; font-size:11px;">{arrow} {abs(change):.2f}%</span></div>', unsafe_allow_html=True)

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:11px; color:#374151;">Data via Yahoo Finance<br>Prices delayed ~15min</div>', unsafe_allow_html=True)

page = st.session_state.page
st.markdown('<div class="top-bar"></div>', unsafe_allow_html=True)

if page == "Stock Lookup":
    lookup.render()
elif page == "Compare Stocks":
    compare.render()
elif page == "Portfolio Simulator":
    portfolio.render()
