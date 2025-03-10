from typing import Dict

def calculate_metrics(data: Dict[str, float]) -> Dict[str, float]:
    """Calcola metriche di value investing."""
    price = data["price"]
    eps = data["eps"]
    book_value = data["book_value"]
    pe_ratio = price / eps if eps != 0 else float('inf')
    pb_ratio = price / book_value if book_value != 0 else float('inf')
    roe = (eps / book_value) * 100 if book_value != 0 else 0
    return {
        "pe_ratio": pe_ratio,
        "pb_ratio": pb_ratio,
        "roe": roe,
        "profit_margin": data["profit_margin"] * 100,
        "dividend_yield": data["dividend_yield"] * 100 if data["dividend_yield"] else 0
    }