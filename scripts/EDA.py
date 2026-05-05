# 1. IMPORT LIBRARIES
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 2. LOAD DATA
df = pd.read_excel(r"C:\Users\bhagawathy manju\OneDrive\Desktop\Sales Dataset.xlsx")
print("First 5 rows:")
print(df.head())

# 3. BASIC INFO + DESCRIPTIVE STATS
print("\nDataset Info:")
print(df.info())

print("\nDescriptive Statistics:")
print(df.describe())


# 4. MISSING VALUES
print("\nMissing Values:")
print(df.isnull().sum())

# 5. NUMERICAL COLUMNS
num_cols = df.select_dtypes(include=['int64', 'float64']).columns
print("\nNumerical Columns:", num_cols)

# 6. HISTOGRAM (DISTRIBUTION)
for col in num_cols:
    plt.figure()
    plt.hist(df[col])
    plt.title(f"Histogram of {col}")
    plt.xlabel(col)
    plt.ylabel("Frequency")
    plt.show()

# 7. BOXPLOT (OUTLIERS)
for col in num_cols:
    plt.figure()
    plt.boxplot(df[col])
    plt.title(f"Boxplot of {col}")
    plt.show()

# 8. SCATTER PLOT
plt.figure()
plt.scatter(df["Amount"], df["Profit"])
plt.xlabel("Amount")
plt.ylabel("Profit")
plt.title("Amount vs Profit")
plt.show()

# 9. CORRELATION + HEATMAP
corr = df[num_cols].corr()

print("\nCorrelation Matrix:")
print(corr)

plt.figure()
sns.heatmap(corr, annot=True)
plt.title("Correlation Heatmap")
plt.show()