# 1. IMPORT LIBRARIES
import pandas as pd
import numpy as np
from scipy import stats

# 2. LOAD DATA
df = pd.read_excel(r"C:\Users\bhagawathy manju\OneDrive\Desktop\Sales Dataset.xlsx")

# 3. SELECT TWO GROUPS (A/B TEST)
# Change category names based on your dataset
group_A = df[df["Category"] == "Electronics"]["Profit"]
group_B = df[df["Category"] == "Furniture"]["Profit"]
print("Electronics count:", len(group_A))
print("Furniture count:", len(group_B))

# 4. CHECK ASSUMPTIONS
# Normality (Shapiro Test)
print("\nNormality Test:")
print("Electronics p:", stats.shapiro(group_A)[1])
print("Furniture p:", stats.shapiro(group_B)[1])
# Variance Equality (Levene Test)
levene_p = stats.levene(group_A, group_B)[1]
print("\nLevene Test p-value:", levene_p)

# 5. T-TEST
t_stat, p_value = stats.ttest_ind(group_A, group_B, equal_var=(levene_p > 0.05))
print("\nT-statistic:", t_stat)
print("P-value:", p_value)

# 6. 95% CONFIDENCE INTERVAL
mean_diff = group_A.mean() - group_B.mean()
se = np.sqrt(group_A.var()/len(group_A) + group_B.var()/len(group_B))
ci_low = mean_diff - 1.96 * se
ci_high = mean_diff + 1.96 * se
print("\nMean Difference:", mean_diff)
print("95% CI:", (ci_low, ci_high))

# 7. INTERPRETATION
if p_value < 0.05:
    print("\nResult: Statistically significant difference (p < 0.05)")
else:
    print("\nResult: No statistically significant difference (p >= 0.05)")