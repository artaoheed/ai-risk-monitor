# src/data/generate_dataset.py
import uuid
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def random_timestamp(start_days=30, n=1):
    base = datetime.utcnow() - timedelta(days=start_days)
    return [(base + timedelta(seconds=random.randint(0, start_days*24*3600))).isoformat()+'Z' for _ in range(n)]

def generate_users(n_users=2000):
    return [f"user_{i:06d}" for i in range(n_users)]

def pick_category():
    cats = ["groceries","crypto","electronics","gift","utilities","travel","gift_card","streaming"]
    weights = [0.25,0.05,0.12,0.08,0.12,0.10,0.05,0.23]
    return random.choices(cats, weights)[0]

def generate_transactions(n_txns=50000, n_users=2000, anomaly_rate=0.02):
    users = generate_users(n_users)
    rows = []
    for _ in range(n_txns):
        txn_id = str(uuid.uuid4())
        user = random.choice(users)
        ts = random_timestamp(start_days=14, n=1)[0]
        amount = round(abs(np.random.exponential(scale=50.0)),2)  # long-tailed
        currency = "USD"
        direction = random.choices(["send","receive"], weights=[0.7,0.3])[0]
        recipient_id = f"r_{random.randint(1,5000)}"
        recipient_type = random.choices(["user","merchant"], weights=[0.6,0.4])[0]
        merchant_category = pick_category()
        origin_geo = random.choices(["US","NG","GB","IN","CA","DE"], weights=[0.6,0.08,0.07,0.12,0.08,0.05])[0]
        dest_geo = random.choices(["US","NG","GB","IN","CA","DE"], weights=[0.6,0.08,0.07,0.12,0.08,0.05])[0]
        channel = random.choices(["mobile","web","api"], weights=[0.8,0.15,0.05])[0]
        device_trust_score = round(np.clip(np.random.normal(0.8, 0.12), 0.0, 1.0), 3)
        # simple user history signals (will be aggregated later or approximated)
        daily_txn_count_user = np.random.poisson(1)
        daily_txn_amount_user = round(daily_txn_count_user * amount * np.random.uniform(0.8,1.2),2)
        is_new_recipient = random.random() < 0.15

        # Decide anomaly
        if random.random() < anomaly_rate:
            label_is_anomaly = 1
            # choose type
            a_type = random.choice(["velocity","geo_mismatch","merchant_risk","high_amount"])
            if a_type == "velocity":
                # simulate many txns quickly (we will tag by anomaly_type; feature engineering later)
                daily_txn_count_user = random.randint(5,20)
                daily_txn_amount_user = round(daily_txn_count_user * amount,2)
            elif a_type == "geo_mismatch":
                origin_geo = random.choice(["CN","RU","BR","NG"])
                dest_geo = random.choice(["US","GB"])
                device_trust_score = round(np.random.uniform(0.0, 0.4),3)
            elif a_type == "merchant_risk":
                merchant_category = "crypto"
                amount = round(amount * random.uniform(2.0, 6.0),2)
            elif a_type == "high_amount":
                amount = round(amount * random.uniform(10,50),2)
            anomaly_type = a_type
        else:
            label_is_anomaly = 0
            anomaly_type = ""

        rows.append({
            "txn_id": txn_id,
            "user_id": user,
            "timestamp": ts,
            "amount": float(amount),
            "currency": currency,
            "direction": direction,
            "recipient_id": recipient_id,
            "recipient_type": recipient_type,
            "merchant_category": merchant_category,
            "origin_geo": origin_geo,
            "dest_geo": dest_geo,
            "channel": channel,
            "device_trust_score": device_trust_score,
            "is_new_recipient": int(is_new_recipient),
            "daily_txn_count_user": int(daily_txn_count_user),
            "daily_txn_amount_user": float(daily_txn_amount_user),
            "label_is_anomaly": int(label_is_anomaly),
            "anomaly_type": anomaly_type
        })
    return pd.DataFrame(rows)

if __name__ == "__main__":
    df = generate_transactions(n_txns=60000, n_users=5000, anomaly_rate=0.025)
    # Shuffle and save
    df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
    out_path = "dataset.csv"
    df.to_csv(out_path, index=False)
    print("Wrote", out_path, "rows:", len(df))
