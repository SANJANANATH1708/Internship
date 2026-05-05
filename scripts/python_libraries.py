# =============================================================================
#  VIZ GALLERY — Matplotlib & Seaborn
#  Topics: Bar, Line + Regression, Scatter, Boxplot, Heatmap
#  Best Practices: titles, labels, legends, color choices
#  Do's and Don'ts documented at the bottom
# =============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from scipy import stats

# ── Reproducibility ──────────────────────────────────────────────────────────
np.random.seed(42)

# ── Global style ─────────────────────────────────────────────────────────────
sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)
plt.rcParams.update({"figure.dpi": 120, "axes.spines.top": False,
                     "axes.spines.right": False})

# =============================================================================
# SAMPLE DATA
# =============================================================================

categories   = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
sales_A      = [4200, 3800, 5100, 4700, 6200, 5800]
sales_B      = [3100, 3500, 4200, 3900, 5100, 4700]

x_scatter    = np.random.normal(50, 15, 120)
y_scatter    = 2.3 * x_scatter + np.random.normal(0, 20, 120)

study_hours  = np.random.uniform(1, 10, 80)
exam_score   = 50 + 5 * study_hours + np.random.normal(0, 5, 80)

departments  = np.repeat(["Engineering", "Marketing", "Sales", "HR", "Design"], 30)
salaries     = np.concatenate([
    np.random.normal(90, 12, 30),
    np.random.normal(72, 10, 30),
    np.random.normal(68, 8,  30),
    np.random.normal(60, 7,  30),
    np.random.normal(75, 11, 30),
])
df_box = pd.DataFrame({"Department": departments, "Salary (k$)": salaries})

features     = ["Feature A", "Feature B", "Feature C", "Feature D", "Feature E"]
corr_data    = pd.DataFrame(np.random.uniform(-1, 1, (5, 5)),
                             columns=features, index=features)
np.fill_diagonal(corr_data.values, 1.0)          # diagonal = 1 (self-correlation)
corr_data    = (corr_data + corr_data.T) / 2     # make symmetric

# =============================================================================
# FIGURE LAYOUT — 2 × 3 grid
# =============================================================================
fig, axes = plt.subplots(2, 3, figsize=(18, 11))
fig.suptitle("Python Visualization Gallery — Matplotlib & Seaborn",
             fontsize=16, fontweight="bold", y=1.01)

# ── 1. BAR CHART ─────────────────────────────────────────────────────────────
ax = axes[0, 0]
x      = np.arange(len(categories))
width  = 0.35

bars_a = ax.bar(x - width/2, sales_A, width, label="Product A",
                color=sns.color_palette("muted")[0], edgecolor="white")
bars_b = ax.bar(x + width/2, sales_B, width, label="Product B",
                color=sns.color_palette("muted")[1], edgecolor="white")

# Value labels on top of each bar
for bar in list(bars_a) + list(bars_b):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 60,
            f"{bar.get_height():,}",
            ha="center", va="bottom", fontsize=8, color="#333333")

ax.set_title("Monthly Sales by Product", fontweight="bold")
ax.set_xlabel("Month")
ax.set_ylabel("Revenue ($)")
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
ax.legend(framealpha=0.3)
ax.set_ylim(0, max(sales_A + sales_B) * 1.18)

# ── 2. LINE CHART ────────────────────────────────────────────────────────────
ax = axes[0, 1]
ax.plot(categories, sales_A, marker="o", linewidth=2.2, markersize=7,
        label="Product A", color=sns.color_palette("muted")[0])
ax.plot(categories, sales_B, marker="s", linewidth=2.2, markersize=7,
        label="Product B", color=sns.color_palette("muted")[1], linestyle="--")

ax.set_title("Sales Trend Over Time", fontweight="bold")
ax.set_xlabel("Month")
ax.set_ylabel("Revenue ($)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
ax.legend(framealpha=0.3)
ax.margins(x=0.05)

# ── 3. SCATTER + REGRESSION LINE ─────────────────────────────────────────────
ax = axes[0, 2]
slope, intercept, r, *_ = stats.linregress(x_scatter, y_scatter)
x_line = np.linspace(x_scatter.min(), x_scatter.max(), 200)
y_line = slope * x_line + intercept

ax.scatter(x_scatter, y_scatter, alpha=0.55, edgecolors="white",
           linewidth=0.5, color=sns.color_palette("muted")[2], label="Observations")
ax.plot(x_line, y_line, color="#e63946", linewidth=2, label=f"Fit (R²={r**2:.2f})")

ax.set_title("Scatter Plot with Regression Line", fontweight="bold")
ax.set_xlabel("Variable X")
ax.set_ylabel("Variable Y")
ax.legend(framealpha=0.3)

# ── 4. SCATTER — study hours vs exam score ────────────────────────────────────
ax = axes[1, 0]
slope2, intercept2, r2, *_ = stats.linregress(study_hours, exam_score)
x_line2 = np.linspace(study_hours.min(), study_hours.max(), 200)

ax.scatter(study_hours, exam_score, alpha=0.6, edgecolors="white",
           color=sns.color_palette("muted")[3], label="Student")
ax.plot(x_line2, slope2 * x_line2 + intercept2,
        color="#e63946", linewidth=2, label=f"Fit (R²={r2**2:.2f})")

ax.set_title("Study Hours vs Exam Score", fontweight="bold")
ax.set_xlabel("Study Hours per Day")
ax.set_ylabel("Exam Score")
ax.legend(framealpha=0.3)

# ── 5. BOXPLOT ───────────────────────────────────────────────────────────────
ax = axes[1, 1]
sns.boxplot(data=df_box, x="Department", y="Salary (k$)",
            palette="muted", width=0.5, linewidth=1.4,
            flierprops={"marker": "o", "markerfacecolor": "grey",
                        "alpha": 0.5, "markersize": 4},
            ax=ax)
ax.set_title("Salary Distribution by Department", fontweight="bold")
ax.set_xlabel("Department")
ax.set_ylabel("Salary (k$)")
ax.tick_params(axis="x", rotation=20)

# ── 6. HEATMAP (Seaborn) ─────────────────────────────────────────────────────
ax = axes[1, 2]
sns.heatmap(corr_data, annot=True, fmt=".2f", cmap="RdBu_r",
            center=0, vmin=-1, vmax=1, linewidths=0.5,
            cbar_kws={"shrink": 0.8, "label": "Correlation"},
            ax=ax)
ax.set_title("Feature Correlation Heatmap", fontweight="bold")
ax.tick_params(axis="x", rotation=30)
ax.tick_params(axis="y", rotation=0)

# ── Final layout ─────────────────────────────────────────────────────────────
plt.tight_layout(pad=2.5)
plt.savefig("viz_gallery.png", bbox_inches="tight", dpi=150)
plt.show()
print("✅ Gallery saved as viz_gallery.png")


# =============================================================================
#  BEST PRACTICES — 3 DO'S & 3 DON'TS
# =============================================================================
"""
✅ DO'S
───────
1. Always add a descriptive TITLE, AXIS LABELS, and LEGEND.
   • Titles tell the story; labels carry units; legends prevent guesswork.
   • Example: ax.set_title(), ax.set_xlabel(), ax.set_ylabel(), ax.legend()

2. Choose COLORBLIND-FRIENDLY palettes (e.g. Seaborn "muted", "colorblind",
   or diverging maps like "RdBu_r" for correlation heatmaps).
   • Avoid red-green combos; always check contrast ratios for accessibility.

3. Use APPROPRIATE chart types for the data:
   • Bar   → comparing discrete categories
   • Line  → trends over continuous time / ordered axis
   • Scatter + regression → relationship / correlation between two variables
   • Boxplot → distribution spread, median, and outliers per group
   • Heatmap → pairwise relationships across many variables at once

❌ DON'TS
──────────
1. DON'T use 3-D charts for 2-D data.
   • Perspective distortion makes values look unequal when they're not.
   • Stick to flat 2-D plots; use facets or subplots for extra dimensions.

2. DON'T omit axis limits or let default scales mislead.
   • A y-axis that starts at a non-zero value can exaggerate small differences.
   • Always justify the scale, or explicitly start from 0 for bar charts.

3. DON'T plot too many series without differentiation.
   • Using only color to distinguish 8+ lines causes confusion.
   • Combine color + line style + markers, and trim to the most important series.
"""