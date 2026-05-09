import yfinance as yf
import pandas as pd


def get_company_name(ticker):
    try:
        info = yf.Ticker(ticker).info
        name = info.get("shortName", None) or info.get("longName", ticker)
        return name
    except:
        return ticker


def get_close(data):
    c = data["Close"].iloc[:, 0] if isinstance(data["Close"], pd.DataFrame) else data["Close"]
    return c.dropna()
