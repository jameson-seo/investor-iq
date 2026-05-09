import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
from utils import get_company_name, get_close


def render():
    st.markdown('<div class="page-title">Stock Lookup</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Search any TSX or NYSE stock for 1-year performance data</div>', unsafe_allow_html=True)

    ticker = st.text_input("", placeholder="Enter ticker — e.g. AAPL, RY.TO, SHOP.TO", key="lookup").upper()

    if ticker:
        with st.spinner(f"Fetching {ticker}..."):
            data = yf.download(ticker, period="1y", auto_adjust=True, progress=False)

        if data.empty:
            st.error(f"Could not find data for '{ticker}'. Check the ticker and try again.")
        else:
            close = get_close(data)
            company = get_company_name(ticker)
            st.markdown(f"<div style='font-size:22px; font-weight:700; color:#f1f5f9; margin-bottom:1rem;'>{ticker} — {company}</div>", unsafe_allow_html=True)

            start_price = float(close.iloc[0])
            end_price = float(close.iloc[-1])
            returns = ((end_price - start_price) / start_price) * 100
            high = float(close.max())
            low = float(close.min())

            col1, col2, col3, col4 = st.columns(4)
            arrow = "▲" if returns >= 0 else "▼"

            price_change = end_price - start_price
            high_diff = high - end_price
            low_diff = end_price - low

            col1.metric("Current Price", f"${end_price:.2f}", f"{'+' if price_change >= 0 else ''}{price_change:.2f} from start")
            col2.metric("1-Year Return", f"{arrow} {returns:.2f}%", f"{returns:.2f}%")
            col3.metric("52-Week High", f"${high:.2f}", f"-${high_diff:.2f} from high" if high_diff > 0.01 else "At 52-week high! 🎉", delta_color="off")
            col4.metric("52-Week Low", f"${low:.2f}", f"+${low_diff:.2f} above low" if low_diff > 0.01 else "At 52-week low", delta_color="normal")

            show_ma = st.checkbox("Show 50-day Moving Average", value=True)

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=close.index, y=close.values,
                mode="lines",
                name="Price",
                fill="tozeroy",
                fillcolor="rgba(14, 165, 233, 0.05)",
                line=dict(color="#0ea5e9", width=2)
            ))

            if show_ma:
                ma50 = close.rolling(window=50).mean()
                fig.add_trace(go.Scatter(
                    x=ma50.index, y=ma50.values,
                    mode="lines", name="50-day MA",
                    line=dict(color="#f59e0b", width=1.5, dash="dot")
                ))

            fig.update_layout(
                title=f"{ticker} — 1 Year Price History",
                xaxis_title="", yaxis_title="Price",
                template="plotly_dark",
                paper_bgcolor="#0f1422",
                plot_bgcolor="#0f1422",
                height=420,
                font=dict(family="Inter", color="#9ca3af"),
                title_font=dict(size=16, color="#f1f5f9"),
                xaxis=dict(gridcolor="#1e2433"),
                yaxis=dict(gridcolor="#1e2433"),
                margin=dict(l=10, r=10, t=50, b=10),
                legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#9ca3af"))
            )
            st.plotly_chart(fig, use_container_width=True)

    else:
        st.markdown("---")
        st.markdown("### Market Overview")

        WATCHLIST = {
            "AAPL": "Apple", "MSFT": "Microsoft", "NVDA": "Nvidia",
            "GOOGL": "Alphabet", "AMZN": "Amazon", "META": "Meta",
            "TSLA": "Tesla", "JPM": "JPMorgan", "BAC": "Bank of America",
            "SPY": "S&P 500 ETF", "QQQ": "Nasdaq ETF",
            "RY.TO": "Royal Bank", "TD.TO": "TD Bank", "BNS.TO": "Scotiabank",
            "SHOP.TO": "Shopify", "ENB.TO": "Enbridge",
            "SU.TO": "Suncor", "CNQ.TO": "Canadian Natural", "XIU.TO": "TSX 60 ETF",
            "NKE": "Nike", "MCD": "McDonald's", "PFE": "Pfizer", "F": "Ford",
            "T": "AT&T", "DIS": "Disney", "NFLX": "Netflix"
        }

        @st.cache_data(ttl=3600)
        def fetch_market_overview(tickers):
            results = []
            for ticker, name in tickers:
                try:
                    data = yf.download(ticker, period="1y", auto_adjust=True, progress=False)
                    if not data.empty:
                        close = data["Close"].iloc[:, 0] if isinstance(data["Close"], pd.DataFrame) else data["Close"]
                        close = close.dropna()
                        ret = ((float(close.iloc[-1]) - float(close.iloc[0])) / float(close.iloc[0])) * 100
                        price = float(close.iloc[-1])
                        results.append({"ticker": ticker, "name": name, "return": ret, "price": price})
                except:
                    pass
                
            return sorted(results, key=lambda x: x["return"], reverse=True)

        with st.spinner("Loading market overview..."):
            results = fetch_market_overview(tuple(WATCHLIST.items()))

        top = results[:5]
        bottom = results[-5:][::-1]

        if "lookup_prefill" not in st.session_state:
            st.session_state.lookup_prefill = ""

        def render_cards(stocks):
            cols = st.columns(5)
            for i, stock in enumerate(stocks):
                actually_positive = stock['return'] >= 0
                color = "#10b981" if actually_positive else "#ef4444"
                border_color = "#10b98130" if actually_positive else "#ef444430"
                arrow = "▲" if actually_positive else "▼"
                cols[i].markdown(f"""
                <div style="
                    background: #0f1422;
                    border: 1px solid {border_color};
                    border-top: 2px solid {color};
                    border-radius: 10px;
                    padding: 1rem;
                    text-align: center;
                ">
                    <div style="font-size:15px; font-weight:700; color:#f1f5f9;">{stock['ticker']}</div>
                    <div style="font-size:11px; color:#4b5563; margin: 3px 0 8px;">{stock['name']}</div>
                    <div style="font-size:13px; color:#6b7280; margin-bottom:4px;">${stock['price']:.2f}</div>
                    <div style="font-size:16px; font-weight:700; color:{color};">{arrow} {abs(stock['return']):.1f}%</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("#### 📈 Top Performers — 1 Year")
        render_cards(top)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 📉 Lowest Performers — 1 Year")
        render_cards(bottom)
