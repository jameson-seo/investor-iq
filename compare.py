import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
from utils import get_company_name, get_close


def render():
    st.markdown('<div class="page-title">Compare Stocks</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Compare performance of two stocks side by side</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    ticker1 = col1.text_input("", placeholder="First ticker — e.g. AAPL", key="t1").upper()
    ticker2 = col2.text_input("", placeholder="Second ticker — e.g. MSFT", key="t2").upper()

    if ticker1 and ticker2:
        with st.spinner("Fetching data..."):
            data1 = yf.download(ticker1, period="1y", auto_adjust=True, progress=False)
            data2 = yf.download(ticker2, period="1y", auto_adjust=True, progress=False)

        if data1.empty or data2.empty:
            st.error("One or both tickers not found.")
        else:
            close1 = get_close(data1)
            close2 = get_close(data2)

            name1 = get_company_name(ticker1)
            name2 = get_company_name(ticker2)

            label1 = f"{ticker1} — {name1}"
            label2 = f"{ticker2} — {name2}"

            start1 = float(close1.iloc[0])
            end1 = float(close1.iloc[-1])
            start2 = float(close2.iloc[0])
            end2 = float(close2.iloc[-1])
            ret1 = ((end1 - start1) / start1) * 100
            ret2 = ((end2 - start2) / start2) * 100

            # Metrics
            mc1, mc2 = st.columns(2)
            mc1.markdown(f"**{label1}**")
            mc1.metric("Start Price", f"${start1:.2f}")
            mc1.metric("Current Price", f"${end1:.2f}")
            mc1.metric("1-Year Return", f"{ret1:.2f}%")

            mc2.markdown(f"**{label2}**")
            mc2.metric("Start Price", f"${start2:.2f}")
            mc2.metric("Current Price", f"${end2:.2f}")
            mc2.metric("1-Year Return", f"{ret2:.2f}%")

            st.markdown("---")

            # Investment simulator
            st.markdown("#### Simulate an Investment")
            inv_col1, inv_col2 = st.columns(2)
            invest1 = inv_col1.number_input(f"$ into {ticker1}", min_value=100, value=1000, step=100)
            invest2 = inv_col2.number_input(f"$ into {ticker2}", min_value=100, value=1000, step=100)

            scaled1 = (close1 / close1.iloc[0]) * invest1
            scaled2 = (close2 / close2.iloc[0]) * invest2

            final1 = float(scaled1.iloc[-1])
            final2 = float(scaled2.iloc[-1])

            res_col1, res_col2 = st.columns(2)
            res_col1.metric(f"{ticker1} final value", f"${final1:,.2f}", round(final1 - invest1, 2))
            res_col2.metric(f"{ticker2} final value", f"${final2:,.2f}", round(final2 - invest2, 2))

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=scaled1.index, y=scaled1.values, mode="lines",
                                     name=ticker1, line=dict(color="#0ea5e9", width=2)))
            fig.add_trace(go.Scatter(x=scaled2.index, y=scaled2.values, mode="lines",
                                     name=ticker2, line=dict(color="#f59e0b", width=2)))
            fig.update_layout(
                title=f"{ticker1} vs {ticker2} — Portfolio Value Over 1 Year",
                template="plotly_dark",
                paper_bgcolor="#0f1422",
                plot_bgcolor="#0f1422",
                height=420,
                font=dict(family="Inter", color="#9ca3af"),
                title_font=dict(size=16, color="#f1f5f9"),
                xaxis=dict(gridcolor="#1e2433"),
                yaxis=dict(gridcolor="#1e2433", tickprefix="$"),
                margin=dict(l=10, r=10, t=50, b=10),
                legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#9ca3af"))
            )
            st.plotly_chart(fig, use_container_width=True)
