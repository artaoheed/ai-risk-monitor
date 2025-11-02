from __future__ import annotations
import argparse, random, csv, time
from datetime import datetime, timedelta
import numpy as np

MERCHANTS = ['p2p','food','ride','gift','withdrawal','crypto']
COUNTRIES = ['US','CA','GB','NG','DE']
def rand_ts(i):
    base = datetime.utcnow() - timedelta(days=7)
    return (base + timedelta(seconds=i*60)).isoformat() + 'Z'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=str, default='data/transactions.csv')
    ap.add_argument('--n', type=int, default=2000)
    ap.add_argument('--seed', type=int, default=42)
    args = ap.parse_args()
    random.seed(args.seed); np.random.seed(args.seed)

    rows = []
    bal = {f'u_{i:06d}': float(random.randint(500, 4000)) for i in range(300)}
    for i in range(args.n):
        uid = random.choice(list(bal.keys()))
        amt = round(max(0.5, np.random.lognormal(mean=4.2, sigma=0.7)), 2)
        ts = rand_ts(i)
        is_night = 1 if random.random() < 0.2 else 0
        device_change_7d = 1 if random.random() < 0.1 else 0
        mc = random.choice(MERCHANTS)
        country = random.choice(COUNTRIES)
        counterparty = f"u_{random.randint(0,999999):06d}"
        rows.append({
            "timestamp": ts,
            "user_id": uid,
            "amount": amt,
            "balance_before": round(bal[uid], 2),
            "device_id": f"d_{random.randint(0,99999):05d}",
            "device_change_7d": device_change_7d,
            "merchant_category": mc,
            "counterparty_id": counterparty,
            "geo_country": country,
            "is_night": is_night
        })
        # update balance
        bal[uid] -= amt * (1 if random.random() < 0.6 else 0.2)
        bal[uid] = max(bal[uid], 0)

    # introduce a few sketchy spikes
    for _ in range(max(5, args.n//200)):
        i = random.randint(0, args.n-1)
        rows[i]["amount"] *= random.uniform(5, 15)
        rows[i]["device_change_7d"] = 1
        rows[i]["is_night"] = 1

    os.makedirs('data', exist_ok=True)
    with open(args.out, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {args.out}")

if __name__ == '__main__':
    import os
    main()
