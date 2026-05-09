import yfinance as yf
import pandas as pd


def get_company_name(ticker):
    KNOWN = {
        "AAPL": "Apple", "MSFT": "Microsoft", "NVDA": "Nvidia",
        "GOOGL": "Alphabet", "AMZN": "Amazon", "META": "Meta",
        "TSLA": "Tesla", "JPM": "JPMorgan", "BAC": "Bank of America",
        "SPY": "S&P 500 ETF", "QQQ": "Nasdaq ETF", "NKE": "Nike",
        "MCD": "McDonald's", "PFE": "Pfizer", "F": "Ford",
        "T": "AT&T", "DIS": "Disney", "NFLX": "Netflix",
        "RY.TO": "Royal Bank", "TD.TO": "TD Bank", "BNS.TO": "Scotiabank",
        "SHOP.TO": "Shopify", "ENB.TO": "Enbridge", "SU.TO": "Suncor",
        "CNQ.TO": "Canadian Natural", "XIU.TO": "TSX 60 ETF"
    }
    if ticker in KNOWN:
        return KNOWN[ticker]
    try:
        info = yf.Ticker(ticker).info
        name = info.get("shortName", None) or info.get("longName", ticker)
        return name
    except:
        return ticker


def get_close(data):
    c = data["Close"].iloc[:, 0] if isinstance(data["Close"], pd.DataFrame) else data["Close"]
    return c.dropna()
