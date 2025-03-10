import yfinance as yf
from typing import Dict
import logging

# Non configuriamo qui, usiamo il logger globale
logger = logging.getLogger(__name__)

def fetch_financial_data(ticker: str) -> Dict[str, float]:
    """Estrae dati quantitativi da yfinance per un’azienda."""
    stock = yf.Ticker(ticker)
    info = stock.info
    data = {
        "price": info.get("currentPrice", 0),
        "eps": info.get("trailingEps", 0),
        "book_value": info.get("bookValue", 0),
        "profit_margin": info.get("profitMargins", 0),
        "dividend_yield": info.get("dividendYield", 0),
        "total_debt": info.get("totalDebt", 0),
        "total_revenue": info.get("totalRevenue", 0),
        "free_cash_flow": info.get("freeCashflow", 0),
        "market_cap": info.get("marketCap", 0),
        "shares_outstanding": info.get("sharesOutstanding", 1)
    }
    # Registra i dati grezzi
    logger.info(f"Dati grezzi per {ticker}: {data}")
    return data