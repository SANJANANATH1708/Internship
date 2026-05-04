import pandas as pd

# ─────────────────────────────────────────────
# STEP 1: CREATE RAW DATA
# ─────────────────────────────────────────────
data = {
    "Product": ["A", "A", "B", "B", "C", "C", "A", "B", "C"],
    "Region": ["north", "south", "north", "south", "north", "south", "east", "east", "east"],
    "Month": ["Jan", "Jan", "Jan", "Jan", "Jan", "Jan", "Feb", "Feb", "Feb"],
    "Sales": [100, 120, 200, 220, 150, 170, 130, 210, 160]
}

df = pd.DataFrame(data)

print("\n🔴 RAW DATA:\n", df)


# ─────────────────────────────────────────────
# STEP 2: DATA CLEANING
# ─────────────────────────────────────────────

# Standardize text format
df["Region"] = df["Region"].str.title()
df["Product"] = df["Product"].str.upper()

print("\n🟢 CLEANED DATA:\n", df)


# ─────────────────────────────────────────────
# STEP 3: FILTERING
# ─────────────────────────────────────────────

# Filter only North region
north_data = df[df["Region"] == "North"]

print("\n🔵 FILTERED DATA (North Region):\n", north_data)


# ─────────────────────────────────────────────
# STEP 4: GROUPING & AGGREGATION
# ─────────────────────────────────────────────

# Product-by-Month summary
product_month = df.groupby(["Product", "Month"])["Sales"].sum().reset_index()

print("\n🟣 PRODUCT BY MONTH:\n", product_month)

# Region-by-Month summary
region_month = df.groupby(["Region", "Month"])["Sales"].sum().reset_index()

print("\n🟡 REGION BY MONTH:\n", region_month)


# ─────────────────────────────────────────────
# STEP 5: PIVOT TABLE
# ─────────────────────────────────────────────

pivot_table = df.pivot_table(
    index="Product",
    columns="Month",
    values="Sales",
    aggfunc="sum"
)

print("\n📊 PIVOT TABLE (Product vs Month):\n", pivot_table)


# ─────────────────────────────────────────────
# STEP 6: UNPIVOT (MELT)
# ─────────────────────────────────────────────

unpivot_data = pd.melt(
    pivot_table.reset_index(),
    id_vars="Product",
    var_name="Month",
    value_name="Sales"
)

print("\n🔁 UNPIVOTED DATA:\n", unpivot_data)