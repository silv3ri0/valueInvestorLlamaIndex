from typing import Dict

def estimate_intrinsic_value(data: Dict[str, float], growth_rate: float = 0.05, discount_rate: float = 0.1, years: int = 10, perpetual_growth: float = 0.02) -> float:
    """Stima il valore intrinseco con un modello DCF, includendo valore terminale."""
    free_cash_flow = data["free_cash_flow"]
    if free_cash_flow <= 0:
        return 0
    # Calcolo dei flussi futuri per i primi 10 anni
    future_cash_flows = [free_cash_flow * ((1 + growth_rate) ** i) for i in range(1, years + 1)]
    # Valore terminale al decimo anno
    terminal_value = future_cash_flows[-1] * (1 + perpetual_growth) / (discount_rate - perpetual_growth)
    # Attualizzazione dei flussi e del valore terminale
    discounted_cash_flows = [cf / ((1 + discount_rate) ** (i + 1)) for i, cf in enumerate(future_cash_flows)]
    discounted_terminal_value = terminal_value / ((1 + discount_rate) ** years)
    # Somma totale
    intrinsic_value = sum(discounted_cash_flows) + discounted_terminal_value
    # Divisione per numero di azioni, se disponibile
    shares_outstanding = data.get("shares_outstanding", 1)  # Default a 1 se non presente
    return intrinsic_value / shares_outstanding

def evaluate_company(metrics: Dict[str, float], intrinsic_value: float, price: float, market_cap: float) -> str:
    """Valuta se l’azienda è sottovalutata o sopravvalutata."""
    pe_ratio = metrics["pe_ratio"]
    pb_ratio = metrics["pb_ratio"]
    roe = metrics["roe"]
    profit_margin = metrics["profit_margin"]
    dividend_yield = metrics["dividend_yield"]
    analysis = [
        f"P/E Ratio: {pe_ratio:.2f}",
        f"P/B Ratio: {pb_ratio:.2f}",
        f"ROE: {roe:.2f}%",
        f"Profit Margin: {profit_margin:.2f}%",
        f"Dividend Yield: {dividend_yield:.2f}%",
        f"Market Cap: ${market_cap / 1e9:.2f}B",
        f"Intrinsic Value per Share: ${intrinsic_value:.2f}"
    ]
    if pe_ratio < 15 and pb_ratio < 1.5:
        analysis.append("Sottovalutata: P/E basso (<15) e P/B ragionevole (<1.5).")
    elif pe_ratio > 20 or pb_ratio > 3:
        analysis.append("Sopravvalutata: P/E alto (>20) o P/B elevato (>3).")
    else:
        analysis.append("Valutazione neutrale basata su P/E e P/B.")
    if roe > 15:
        analysis.append("Buon ROE (>15%), segno di efficienza.")
    if profit_margin > 10:
        analysis.append("Margini di profitto solidi (>10%).")
    if dividend_yield > 2:
        analysis.append("Dividendo attraente (>2%).")
    if intrinsic_value > price:
        analysis.append(f"Sottovalutata: Valore intrinseco per azione (${intrinsic_value:.2f}) > Prezzo (${price:.2f}).")
    elif intrinsic_value < price:
        analysis.append(f"Sopravvalutata: Valore intrinseco per azione (${intrinsic_value:.2f}) < Prezzo (${price:.2f}).")
    return "\n".join(analysis)