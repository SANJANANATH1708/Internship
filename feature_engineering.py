# 1. IMPORT LIBRARIES
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# 2. LOAD DATA
df = pd.read_excel(r"C:\Users\bhagawathy manju\OneDrive\Desktop\Daily Household Transactions.csv.xlsx")

print("Columns:", df.columns)
print(df.head())

# 3. DATA CLEANING
# Convert Date
df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
# Keep only Expense (ignore transfers/income for RFM)
df = df[df["Income/Expense"] == "Expense"]
# Remove missing values
df = df.dropna()

# 4. CREATE RFM FEATURES (mode)
# Reference date
reference_date = df["Date"].max()
# Correct RFM
rfm = df.groupby("Mode").agg(
    Recency=("Date", lambda x: (reference_date - x.max()).days),
    Frequency=("Amount", "count"),
    Monetary=("Amount", "sum")
).reset_index()
print("\nRFM Data:")
print(rfm)

# 5. ENCODING (CATEGORY)
df_encoded = pd.get_dummies(df, columns=["Category"])

# 6. SCALING
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm[["Recency", "Frequency", "Monetary"]])

# 7. CLUSTERING (WITH RFM)
kmeans = KMeans(n_clusters=3, random_state=42)
rfm["Cluster"] = kmeans.fit_predict(rfm_scaled)
print("\nClusters with RFM:")
print(rfm)

# 8. CLUSTERING (WITHOUT FEATURE ENGINEERING)
basic_data = df[["Amount"]]

basic_scaled = scaler.fit_transform(basic_data)
kmeans_basic = KMeans(n_clusters=3, random_state=42)
basic_data["Cluster"] = kmeans_basic.fit_predict(basic_scaled)
print("\nBasic Clustering:")
print(basic_data.head())

# 9. SAVE OUTPUT
rfm.to_csv("rfm_output.csv", index=False)
basic_data.to_csv("basic_output.csv", index=False)
print("\n✅ Feature Engineering Completed!")