import pandas as pd
import numpy as np

# Step 1: Read the CSV file
pdf = pd.read_csv("aave-v2-health-factor-complete.csv")

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

target = ["HF"]
minimal_features = [
    "total_collateral_eth",
    "current_liquidation_threshold",
    "available_borrows_eth",
    "total_debt_eth",
]
columns = [*minimal_features, *target, "address", "block_timestamp"]
df = pdf[0:100000]
df = df[pd.Index(columns)]
df["block_timestamp"] = pd.to_datetime(df["block_timestamp"])
df.sort_values(by=["address", "block_timestamp"], inplace=True)


def create_features(group, window_size):
    group["avg_hf"] = group["HF"].rolling(window=window_size).mean()
    group["median_hf"] = group["HF"].rolling(window=window_size).median()
    group["hf_change"] = group["HF"].diff()
    group["hf_trend"] = group["hf_change"].rolling(window=window_size).sum()
    return group


# Optimized feature engineering
df = create_features(df, window_size=5)


# Function to create sequences with optimized operations
def create_sequences_optimized(df, window_size=5):
    sequences = []
    targets = []
    for address, group in df.groupby("address"):
        total_rows = len(group)
        for i in range(window_size, total_rows):
            sequence = group.iloc[i - window_size : i - 1][
                pd.Index(minimal_features)
            ].values
            target = 1.0 if group.iloc[i]["HF"] < 1 else 0.0
            sequences.append(sequence)
            targets.append(target)
    return np.array(sequences), np.array(targets)


X, y = create_sequences_optimized(df, window_size=6)

np.save("XC.npy", X)
np.save("yC.npy", y)
