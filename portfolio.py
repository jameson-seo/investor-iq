import streamlit as st
import yfinance as yf
import pandas as pd
from utils import get_company_name, get_close


def render():
    st.markdown('<div class="page-title">Portfolio Simulator</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Add stocks and see what your return would have been over the past year</div>', unsafe_allow_html=True)

    st.info("Enter a ticker (e.g. AAPL, RY.TO) and number of shares, then click Add Stock.")

    if "portfolio" not in st.session_state:
        st.session_state.portfolio = []

    col1, col2, col3 = st.columns([3, 1, 1])
    new_ticker = col1.text_input("", placeholder="Stock ticker — e.g. AAPL, RY.TO").upper()
    new_shares = col2.number_input("Shares", min_value=1, value=10)
    col3.markdown("<br>", unsafe_allow_html=True)
    if col3.button("Add Stock", use_container_width=True):
        if new_ticker:
            test = yf.download(new_ticker, period="5d", auto_adjust=True, progress=False)
            if test.empty:
                st.error(f"Could not find '{new_ticker}' — check the ticker and try again.")
            else:
                company = get_company_name(new_ticker)
                st.session_state.portfolio.append({"ticker": new_ticker, "shares": new_shares, "company": company})
                st.success(f"Added {new_ticker} × {new_shares} shares — {company}")
    if st.button("Clear Portfolio"):
        st.session_state.portfolio = []

    if st.session_state.portfolio:
        st.markdown("---")
        total_start = 0
        total_end = 0
        rows = []
        to_delete = None

        for i, item in enumerate(st.session_state.portfolio):
            ticker = item["ticker"]
            company = item.get("company", ticker)
            shares = item["shares"]

            data = yf.download(ticker, period="1y", auto_adjust=True, progress=False)
            if not data.empty:
                close = get_close(data)
                start_price = float(close.iloc[0])
                end_price = float(close.iloc[-1])
                start_value = start_price * shares
                end_value = end_price * shares
                ret = ((end_value - start_value) / start_value) * 100
                total_start += start_value
                total_end += end_value
                rows.append({
                    "index": i,
                    "Ticker": f"{ticker} — {company}",
                    "Shares": shares,
                    "Start Value": f"${start_value:,.2f}",
                    "Current Value": f"${end_value:,.2f}",
                    "Return": f"{ret:.2f}%"
                })
            else:
                st.warning(f"Could not find {ticker} — skipping.")

        # Table header
        header = st.columns([4, 1, 2, 2, 2, 1])
        headers = ["Ticker", "Shares", "Start Value", "Current Value", "Return", ""]
        for col, h in zip(header, headers):
            col.markdown(f"<span style='font-size:16px; font-weight:600; color:#4b5563; text-transform:uppercase; letter-spacing:0.5px;'>{h}</span>", unsafe_allow_html=True)

        st.markdown("<hr style='border-color:#1e2433; margin: 0.3rem 0;'>", unsafe_allow_html=True)

        # Table rows
        for row in rows:
            ret_val = float(row["Return"].replace("%", ""))
            ret_color = "#10b981" if ret_val >= 0 else "#ef4444"
            cols = st.columns([4, 1, 2, 2, 2, 1])
            cols[0].markdown(f"<span style='color:#f1f5f9; font-size:16px;'>{row['Ticker']}</span>", unsafe_allow_html=True)
            cols[1].markdown(f"<span style='color:#9ca3af; font-size:16px;'>{row['Shares']}</span>", unsafe_allow_html=True)
            cols[2].markdown(f"<span style='color:#9ca3af; font-size:16px;'>{row['Start Value']}</span>", unsafe_allow_html=True)
            cols[3].markdown(f"<span style='color:#9ca3af; font-size:16px;'>{row['Current Value']}</span>", unsafe_allow_html=True)
            cols[4].markdown(f"<span style='color:{ret_color}; font-size:16px; font-weight:600;'>{row['Return']}</span>", unsafe_allow_html=True)
            if cols[5].button("Remove", key=f"del_{row['index']}"):
                to_delete = row["index"]

            st.markdown("<hr style='border-color:#1e2433; margin: 0.3rem 0;'>", unsafe_allow_html=True)

        # Total row
        if total_start > 0:
            total_return = ((total_end - total_start) / total_start) * 100
            total_color = "#10b981" if total_return >= 0 else "#ef4444"
            total_cols = st.columns([4, 1, 2, 2, 2, 1])
            total_cols[0].markdown(f"<span style='color:#f1f5f9; font-size:16px; font-weight:700;'>TOTAL</span>", unsafe_allow_html=True)
            total_cols[1].markdown("", unsafe_allow_html=True)
            total_cols[2].markdown(f"<span style='color:#f1f5f9; font-size:16px; font-weight:700;'>${total_start:,.2f}</span>", unsafe_allow_html=True)
            total_cols[3].markdown(f"<span style='color:#f1f5f9; font-size:16px; font-weight:700;'>${total_end:,.2f}</span>", unsafe_allow_html=True)
            total_cols[4].markdown(f"<span style='color:{total_color}; font-size:16px; font-weight:700;'>{total_return:.2f}%</span>", unsafe_allow_html=True)
            total_cols[5].markdown("", unsafe_allow_html=True)

        if to_delete is not None:
            st.session_state.portfolio.pop(to_delete)
            st.rerun()

        # Portfolio Summary
        if total_start > 0:
            profit = total_end - total_start
            total_return = ((total_end - total_start) / total_start) * 100
            st.markdown("### Portfolio Summary")
            col1, col2, col3 = st.columns(3)
            col1.metric("Start Value", f"${total_start:,.2f}")
            col2.metric("Current Value", f"${total_end:,.2f}")
            col3.metric("Total Return", f"{total_return:.2f}%", round(profit, 2))

    else:
        st.markdown('<div style="color:#4b5563; font-size:15px; padding: 2rem 0;">No stocks added yet. Use the form above to build your portfolio.</div>', unsafe_allow_html=True)
