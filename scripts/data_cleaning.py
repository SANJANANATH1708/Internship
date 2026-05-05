import pandas as pd
import numpy as np

# 1. CREATE DIRTY DATASET
data = {
    "Name": [" Alice ", "bob", "CHARLIE", None, "Eve", "Alice"],
    "Age": [25, None, 30, 22, None, 25],
    "Join_Date": ["2023-01-01", "01/02/2023", "March 3 2023", None, "2023/05/01", "2023-01-01"],
    "Department": ["HR", "IT", None, "Finance", "IT", "HR"]
}

df = pd.DataFrame(data)

df.to_csv("dirty_data.csv", index=False)
print("\n🔴 ORIGINAL DATA:\n", df)

# 2. DATA CLEANING
# Clean names
df["Name"] = df["Name"].str.strip().str.title()
# Standardize dates
df["Join_Date"] = pd.to_datetime(df["Join_Date"], errors="coerce")
# Fill missing department
df["Department"] = df["Department"].fillna("Unknown")

print("\n🟢 CLEANED DATA:\n", df)

# 3. METHOD 1: DROP MISSING VALUES
df_drop = df.dropna()
print("\n🔵 AFTER DROPPING MISSING VALUES:\n", df_drop)

# 4. METHOD 2: FILL MISSING VALUES
df_fill = df.copy()
# Fill Age with mean
df_fill["Age"] = df_fill["Age"].fillna(df_fill["Age"].mean())
# Fill Name with Unknown
df_fill["Name"] = df_fill["Name"].fillna("Unknown")
print("\n🟣 AFTER FILLING VALUES:\n", df_fill)

# 5. REMOVE DUPLICATES
df_final = df_fill.drop_duplicates()
print("\n🟡 FINAL CLEAN DATA:\n", df_final)

# 6. COMPARISON
print("\n📊 DATASET SIZE COMPARISON:")
print("Original:", df.shape)
print("After Drop:", df_drop.shape)
print("After Fill:", df_fill.shape)