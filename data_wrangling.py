# 1. IMPORT LIBRARY
import pandas as pd

# 2. LOAD DATA
df = pd.read_excel(r"C:\Users\bhagawathy manju\OneDrive\Desktop\Sales Dataset.xlsx")

print("Raw Data:")
print(df.head())

# 3. DATA CLEANING
# Remove missing values
df = df.dropna()
# Remove extra spaces
df["Category"] = df["Category"].str.strip()
df["State"] = df["State"].str.strip()
df["City"] = df["City"].str.strip()
df["CustomerName"] = df["CustomerName"].str.strip()
print("\nCleaned Data:")
print(df.head())



# 4. DATA TRANSFORMATION
df = df[df["Amount"] > 0]
# Convert date column (if needed)
df["Order Date"] = pd.to_datetime(df["Order Date"], errors='coerce')
# Create Year-Month column (if not already correct)
df["Year-Month"] = df["Order Date"].dt.to_period("M")
print("\nTransformed Data:")
print(df.head())

# 5. AGGREGATION
# Category-wise monthly sales
category_month = df.groupby(["Category", "Year-Month"])["Amount"].sum().reset_index()
# State-wise monthly sales
state_month = df.groupby(["State", "Year-Month"])["Amount"].sum().reset_index()
print("\nCategory-Month Summary:")
print(category_month)
print("\nState-Month Summary:")
print(state_month)

# 6. PIVOT TABLE
pivot_table = df.pivot_table(
    values="Amount",
    index="Category",
    columns="Year-Month",
    aggfunc="sum"
)

print("\nPivot Table:")
print(pivot_table)

# 7. UNPIVOT (MELT)
unpivot = pivot_table.reset_index().melt(
    id_vars="Category",
    var_name="Year-Month",
    value_name="Amount"
)
print("\nUnpivoted Data:")
print(unpivot)

# 8. SAVE OUTPUT FILES
category_month.to_csv("category_month_summary.csv", index=False)
state_month.to_csv("state_month_summary.csv", index=False)
pivot_table.to_csv("pivot_table.csv")
unpivot.to_csv("unpivot_data.csv", index=False)

print("\n All files saved successfully!")