from __future__ import annotations
import argparse, joblib, pandas as pd
from sklearn.ensemble import IsolationForest
from src.utils.io import load_transactions, to_features
from src.utils.risk import score_to_0_100

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', type=str, required=True)
    ap.add_argument('--out', type=str, default='artifacts/isoforest.joblib')
    ap.add_argument('--n_estimators', type=int, default=200)
    ap.add_argument('--contamination', type=float, default=0.02)
    args = ap.parse_args()

    df = load_transactions(args.input)
    X = to_features(df).values

    model = IsolationForest(
        n_estimators=args.n_estimators,
        contamination=args.contamination,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X)

    os.makedirs('artifacts', exist_ok=True)
    joblib.dump(model, args.out)
    print(f"Saved model to {args.out}")

if __name__ == '__main__':
    import os
    main()
