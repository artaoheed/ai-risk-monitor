# Data Dictionary — dataset.csv

| Column | Type | Description | Example | Notes |
|---|---:|---|---|---|
| txn_id | STRING | Unique transaction identifier | 123e4567-e89b-12d3 | Primary key |
| user_id | STRING | Synthetic user id | user_000123 | Pseudonymous |
| timestamp | TIMESTAMP | Transaction time (UTC ISO 8601) | 2025-11-03T12:34:56Z | |
| amount | FLOAT | Transaction amount in USD | 125.50 | Heavy-tailed distribution |
| currency | STRING | Currency code | USD | All synthetic values default USD |
| direction | STRING | send or receive | send | |
| recipient_id | STRING | Recipient identifier | r_2345 | Pseudonymous |
| recipient_type | STRING | user or merchant | merchant | |
| merchant_category | STRING | Category label | crypto | Used for 'merchant_risk' anomalies |
| origin_geo | STRING | Origin country code | US | |
| dest_geo | STRING | Destination country | NG | |
| channel | STRING | Channel used | mobile | |
| device_trust_score | FLOAT | Simulated device trust (0-1) | 0.92 | Lower scores indicate untrusted device |
| is_new_recipient | INTEGER | 1 if recipient is new to user | 1 | |
| daily_txn_count_user | INTEGER | Count transactions that day for user | 3 | Aggregated approximation |
| daily_txn_amount_user | FLOAT | Sum of amounts that day | 250.00 | |
| label_is_anomaly | INTEGER | 0 normal, 1 anomalous | 1 | Ground truth from generator |
| anomaly_type | STRING | Taxonomy label | velocity | One of (velocity, geo_mismatch, merchant_risk, high_amount) |
