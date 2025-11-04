import pandas as pd
df = pd.read_csv("dataset.csv")
df.info()
df.label_is_anomaly.value_counts()
df.groupby("anomaly_type").size()
df.amount.describe()
