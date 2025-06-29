**Tangnet Project: AI Stock Market Simulator (Phase 1 Planning)**

---

### 📈 Concept Overview

Create a network of Pi and PC nodes on Tangnet, each simulating an investor with an AI profile. Feed the system real-time and historical market data, and simulate:

* Buy/sell decisions
* Portfolio changes
* Sentiment shifts

Eventually, you can use this to:

* Predict short-term movements
* Test trading strategies
* Visualize AI behavior as a real-time market

---

### 📊 Phase 1 Goals

**System Scope:**

* 1–2 Raspberry Pi 5s (7B LLaMA models, low-frequency polling)
* 1 Windows Desktop (RTX 3070 Ti) as master coordinator and frontend
* Use real or mock data (e.g., Yahoo Finance, Alpaca, Finnhub, or local CSV logs)

**Use Case:**

* Ask Tangnet: "What should investor node #12 do about NVDA?"
* Get short narrative + suggested trade

---

### ⚖️ Tech Stack

| Component      | Tool/Library                                 |
| -------------- | -------------------------------------------- |
| Real-Time Data | `yfinance`, `alpaca-py`, `polygon.io`, etc.  |
| Historical Sim | CSV logs or SQLite w/ tick-level history     |
| Local AI Logic | `llama.cpp` or `ollama` CLI                  |
| Orchestration  | Python3 + shell scripts                      |
| Visualization  | Flask, React (dashboard), D3.js, or Plotly   |
| Communication  | SSH / Tailscale Mesh / Python REST endpoints |
| State Mgmt     | JSON / SQLite / custom JSON portfolio files  |

---

### 🎡 Investor Node Template (LLaMA Prompt)

```text
You are Investor-12. Your profile is "aggressive day trader, tech-focused".
Given the following stock data, make a short-term recommendation.

Stock: NVDA
Current Price: $120
Yesterday's Close: $123
Sentiment Score: -0.3
Volume: 1.2x average

What should you do today?
```

*LLM returns:*

```text
"I believe NVDA is experiencing a small dip due to market-wide tech correction.
If the volume holds, a rebound may occur by EOD. Buy 5 shares at $120 limit."
```

---

### 🚀 Future Scaling Ideas

* Assign each Pi a specific investor personality and stock sector
* Enable battle royale simulation of "smartest trader wins"
* Connect to TradingView API or Alpaca for paper trading
* Run "market days" where all nodes simulate a session based on 1-day data snapshot
* Add reinforcement learning (Q-learning) for adaptive models

---

### 💎 Monetization Ideas

* Showcase visual dashboard for demo purposes
* Offer it as a teaching tool or AI investing sandbox (freemium model)
* Sell trader profile packs, pre-tuned LLM agents, or "market crash" scenarios

---

### ⚡ Quick Wins

* Start with mock JSON data + 1 Pi + 1 Desktop for testing
* Build Flask dashboard to visualize node trades
* Write prompt templates and randomize investor behavior with seed
* Add simple portfolio tracker (cash, shares, unrealized PnL)

---

Want help building the initial prompt processor and Flask dashboard starter?
