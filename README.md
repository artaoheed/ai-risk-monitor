# AI Risk Monitor for Cash App Users

An 8-day sprint project that demonstrates how to combine **anomaly detection** with an **LLM explanation layer** to help users understand *why* a transfer might look suspicious — without violating trust.

## ✨ What this repo contains
- **Model**: Isolation Forest baseline + risk score
- **LLM layer**: Prompted, friendly explanations (stubbed locally; can swap to your provider)
- **Dashboard**: Streamlit app for uploading a CSV and reviewing flagged transactions
- **Synthetic data**: Generator script for realistic-but-fake transaction streams
- **Ethics notes**: UX guardrails and model limitations

## 🔧 Tech
- Python 3.10+
- pandas, scikit-learn, pyod (optional), streamlit, pydantic, python-dotenv

## 🚀 Quickstart
```bash
# 1) Create & activate venv (example for macOS/Linux)
python -m venv .venv && source .venv/bin/activate
# On Windows: .venv\Scripts\activate

# 2) Install deps
pip install -r requirements.txt

# 3) (Optional) Set your LLM provider keys
cp .env.example .env
# Edit .env and set PROVIDER + API keys if using live LLM

# 4) Generate synthetic data
python src/data/generate_synthetic.py --out data/transactions.csv --seed 42 --n 5000

# 5) Train baseline model
python src/models/train_isoforest.py --input data/transactions.csv --out artifacts/isoforest.joblib

# 6) Run the dashboard
streamlit run app/streamlit_app.py
```

## 🗂️ Repository layout
```
ai-risk-monitor/
├─ app/
│  └─ streamlit_app.py
├─ src/
│  ├─ data/
│  │  └─ generate_synthetic.py
│  ├─ llm/
│  │  ├─ explain.py
│  │  └─ prompts.py
│  ├─ models/
│  │  └─ train_isoforest.py
│  └─ utils/
│     ├─ io.py
│     └─ risk.py
├─ prompts/
│  └─ explanation_prompt.md
├─ notebooks/
│  └─ exploration.ipynb
├─ assets/
│  └─ architecture.mmd
├─ .github/workflows/
│  └─ ci.yml
├─ .env.example
├─ requirements.txt
├─ LICENSE
└─ README.md
```

## 📊 Features & assumptions
- **Risk score** in [0,100]; threshold configurable in UI
- LLM explanations are **post-hoc** and **non-authoritative** (never auto-block)
- **User control first**: users can mark alerts as helpful/not-helpful → log to CSV
- Works on **synthetic data only** for demo; no real Cash App data

## 🧪 Example CSV schema
| column | type | example |
|---|---|---|
| timestamp | ISO-8601 | 2025-01-02T09:31:02Z |
| user_id | str | u_000123 |
| amount | float | 185.25 |
| balance_before | float | 1200.50 |
| device_id | str | d_aa33 |
| device_change_7d | int | 1 |
| merchant_category | str | p2p |
| counterparty_id | str | u_998877 |
| geo_country | str | US |
| is_night | int (0/1) | 0 |

> You can add more features like **velocity** (transfers per 1/6/24 hours), **geo jumps**, **chargeback history**, etc.

## 🔒 Ethics & guardrails
- **No auto-blocking**; alerts are recommendations with rationale
- **Calm language**: avoid fear-inducing copy
- **Opt-out** controls; feedback loop for false positives
- **Privacy**: synthetic data only; never log user secrets

## 🧭 Roadmap / What I’d do in the fellowship
- Calibrate thresholds per persona; cost-sensitive learning
- Add graph-level features (device graph, counterparty graph)
- RAG over risk policies for more grounded explanations
- Red-team prompts for prompt injection & jailbreaks
- Comprehensive eval harness (precision@k, alert fatigue metrics)

---

**Author:** Taoheed @artaoheed • MIT License
