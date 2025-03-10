# 📊 Value Investing Analyzer

Uno strumento avanzato per l'analisi delle aziende secondo i principi del **value investing**, ispirato all'approccio di **Warren Buffett**. Questo progetto utilizza **yFinance** per ottenere dati finanziari e **LlamaIndex con DeepSeek LLM** per fornire un'analisi approfondita.

---

## ⚡ Funzionalità
- 📊 **Estrazione dati finanziari**: recupera dati chiave di un'azienda quotata (es. prezzo, P/E, P/B, ROE, market cap, ecc.).
- 💡 **Calcolo delle metriche**: applica formule per ottenere parametri di valore intrinseco.
- 🎡 **Valutazione aziendale**: determina se una società è sottovalutata o sopravvalutata.
- 🧪 **Automazione con LLM**: utilizza **DeepSeek AI** per generare una valutazione qualitativa basata sui dati estratti.

---

## 🛠️ Installazione
### 1. Clona il repository
```bash
git clone https://github.com/TUO-USERNAME/value-investing-analyzer.git
cd value-investing-analyzer
```

### 2. Crea un ambiente virtuale e installa le dipendenze
```bash
python -m venv venv
source venv/bin/activate  # Su Windows usa: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configura il file `.env`
Crea un file `.env` copiando il modello `.env.example`:
```bash
cp .env.example .env
```
E modifica il valore della tua **DeepSeek API key**:
```
DEEPSEEK_API_KEY=your_api_key_here
```

### 4. Esegui l'analisi
```bash
python main.py
```

---

## 📊 Esempio di Output
```bash
Starting analysis for AAPL...
Intrinsic value: $145.20
Market price: $150.30
🚨 Apple è SOPRAVVALUTATA!
```

---

## 💡 Struttura del Progetto
```
value-investing-analyzer/
│── tools/
│   ├── data_fetcher.py       # Estrazione dati finanziari
│   ├── metrics.py            # Calcolo parametri value investing
│   ├── valuation.py          # Valutazione finale della società
│── .gitignore                # Esclude file sensibili
│── .env.example              # Template per variabili d'ambiente
│── README.md                 # Documentazione del progetto
│── requirements.txt          # Dipendenze Python
│── main.py                   # Script principale
```

---

## 🔄 Workflow del Codice
1. **`fetch_financial_data()`**: Ottiene dati da yFinance.
2. **`calculate_metrics()`**: Calcola indicatori finanziari.
3. **`estimate_intrinsic_value()`**: Determina il valore intrinseco con il modello DCF.
4. **`evaluate_company()`**: Confronta il valore intrinseco con il prezzo di mercato.
5. **`DeepSeekLLM.complete()`**: Chiede a un LLM di fornire un giudizio qualitativo basato sui dati estratti.

---

## 💪 Contributi
- Sentiti libero di aprire **issue** o **pull request** per migliorare il progetto!
- Idee di sviluppo:
  - ✅ Aggiungere supporto per altre fonti dati (AlphaVantage, Finnhub)
  - ✅ Implementare test automatizzati con `pytest`
  - ✅ Integrazione con una dashboard interattiva (es. Streamlit o Dash)

---

💚 **Licenza:** MIT

🌟 **Autore:** Silverio Giancristofaro

