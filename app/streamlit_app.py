import os
import pandas as pd
import streamlit as st
import joblib
from src.utils.io import load_transactions, to_features
from src.utils.risk import score_to_0_100
from src.llm.explain import explain

st.set_page_config(page_title="AI Risk Monitor", layout="wide")

st.title("🛡️ AI Risk Monitor (Demo)")
st.caption("Synthetic data • Post-hoc explanations • Calm, trust-first copy")


uploaded = st.file_uploader("Upload transactions CSV", type=["csv"])
threshold = st.slider("Alert threshold (0-100)", min_value=0, max_value=100, value=85)
model_path = st.text_input("Model path", value="artifacts/isoforest.joblib")

col_l, col_r = st.columns([2,1])

with col_r:
    st.markdown("### How it works")
    st.markdown("""- We compute features per transaction
- A baseline Isolation Forest scores anomalies
- Scores are normalized to 0–100
- LLM layer explains flagged items in plain language
- You remain in control: alerts are suggestions, not blocks
""")

if uploaded is not None:
    df = pd.read_csv(uploaded)
    st.subheader("Preview")
    st.dataframe(df.head(10))

    # Features
    X = to_features(df)
    st.markdown("**Engineered features (sample)**")
    st.dataframe(X.head(10))

    # Model
    if not os.path.exists(model_path):
        st.error(f"Model not found at {model_path}. Train it first.")
        st.stop()
    model = joblib.load(model_path)
    scores = -model.score_samples(X.values)  # higher = more anomalous
    risks = score_to_0_100(scores)

    out = df.copy()
    out["risk_score"] = risks
    flagged = out[out["risk_score"] >= threshold].copy()

    st.metric("Total transactions", len(out))
    st.metric("Flagged (>= threshold)", len(flagged))

    st.subheader("Flagged transactions")
    if len(flagged) == 0:
        st.success("No items exceed the current threshold.")
    else:
        # Generate explanations
        messages = []
        for _, row in flagged.iterrows():
            features = {
                "risk_score": float(row["risk_score"]),
                "amount": float(row["amount"]),
                "timestamp": str(row["timestamp"]),
                "geo_country": str(row.get("geo_country","")),
                "device_change_7d": int(row.get("device_change_7d",0)),
                "is_night": int(row.get("is_night",0)),
                "notes": "demo"
            }
            messages.append(explain(features))
        flagged["explanation"] = messages
        st.dataframe(flagged[["timestamp","user_id","amount","merchant_category","geo_country","risk_score","explanation"]])

        st.download_button("Download flagged CSV", data=flagged.to_csv(index=False).encode("utf-8"),
                           file_name="flagged_transactions.csv", mime="text/csv")
else:
    st.info("Upload a CSV to begin.")
