from __future__ import annotations
import pandas as pd
from pydantic import BaseModel, Field, ValidationError

REQUIRED_COLUMNS = [
    "timestamp","user_id","amount","balance_before","device_id",
    "device_change_7d","merchant_category","counterparty_id",
    "geo_country","is_night"
]

class InputSchema(BaseModel):
    timestamp: str
    user_id: str
    amount: float
    balance_before: float
    device_id: str
    device_change_7d: int
    merchant_category: str
    counterparty_id: str
    geo_country: str
    is_night: int

def load_transactions(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    return df

def to_features(df: pd.DataFrame) -> pd.DataFrame:
    # Minimal feature engineering demo
    out = pd.DataFrame()
    out["amount"] = df["amount"].astype(float)
    out["balance_ratio"] = (df["amount"] / (df["balance_before"].abs() + 1e-6)).clip(0, 10.0)
    out["is_night"] = df["is_night"].astype(int)
    out["device_change_7d"] = df["device_change_7d"].astype(int)
    # one-hot merchant_category (top K only)
    top_mc = df["merchant_category"].value_counts().nlargest(5).index
    for m in top_mc:
        out[f"mc_{m}"] = (df["merchant_category"] == m).astype(int)
    return out
