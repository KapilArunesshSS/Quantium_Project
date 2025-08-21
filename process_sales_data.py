import pandas as pd
import os

# Input CSVs
files = [
    "data/daily_sales_data_0.csv",
    "data/daily_sales_data_1.csv",
    "data/daily_sales_data_2.csv"
]

# Make sure output folder exists
os.makedirs("output", exist_ok=True)

dfs = []

for file in files:
    df = pd.read_csv(file)

    # Only keep Pink Morsels
    df = df[df["product"] == "pink morsel"]

    # Compute Sales
    df["Sales"] = df["quantity"] * df["price"]

    # Keep only required columns
    df = df[["Sales", "date", "region"]]

    dfs.append(df)

# Combine all into one DataFrame
final_df = pd.concat(dfs, ignore_index=True)

# Save inside output/ folder
output_path = "output/output.csv"
final_df.to_csv(output_path, index=False)

print(f"Output saved to {output_path}")
