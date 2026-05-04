# 1. IMPORT LIBRARY
import pandas as pd

# 2. LOAD DATA
df = pd.read_excel(r"C:\Users\bhagawathy manju\OneDrive\Desktop\Sales Dataset.xlsx")

print("Raw Data:")
print(df.head())

# 3. CLEANING
df = df.dropna()

df["Category"] = df["Category"].str.strip()
df["State"] = df["State"].str.strip()
df["City"] = df["City"].str.strip()
# Convert date
df["Order Date"] = pd.to_datetime(df["Order Date"], errors='coerce')
print("\nCleaned Data:")
print(df.head())

# 4. FILTERING
# Keep only sales above 1000
filtered_df = df[df["Amount"] > 1000]

print("\nFiltered Data (Amount > 1000):")
print(filtered_df.head())

# 5. BUSINESS RULES
# Rule 1: Add Tax (10%)
df["Tax"] = df["Amount"] * 0.10

# Rule 2: Final Amount after tax
df["Final Amount"] = df["Amount"] + df["Tax"]

# Rule 3: Rename Category (example)
df["Category"] = df["Category"].replace({
    "Electronics": "Electronic Goods"
})

# Log transformations
print("\nBusiness Rules Applied:")
print(df[["Amount", "Tax", "Final Amount", "Category"]].head())

# 6. GROUPING (MULTI-LEVEL)
# Region + Category (using State as Region)
grouped = df.groupby(["State", "Category"])["Final Amount"].sum().reset_index()

print("\nState + Category Summary:")
print(grouped)

# 7. RANKING CATEGORIES
# Total sales per category
category_total = df.groupby("Category")["Final Amount"].sum().reset_index()
# Rank categories based on contribution
category_total["Rank"] = category_total["Final Amount"].rank(ascending=False)
print("\nCategory Ranking:")
print(category_total.sort_values("Rank"))

# 8. SAVE OUTPUT
grouped.to_csv("state_category_summary.csv", index=False)
category_total.to_csv("category_ranking.csv", index=False)
print("\nTask Completed Successfully")

