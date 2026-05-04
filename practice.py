
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patches as FancyBboxPatch
from matplotlib.patches import FancyBboxPatch
from matplotlib.gridspec import GridSpec
import matplotlib.patheffects as pe
import warnings
warnings.filterwarnings("ignore")

# CONFIG
EXCEL_PATH = r"C:\Users\bhagawathy manju\OneDrive\Desktop\INTERNSHIP\Replica of Internship Master.xlsx"
SHEET_NAME = "Main"

#COLORS
BG          = "#0a0f1e"
CARD        = "#1e293b"
BORDER      = "#1e3a5f"
TEXT_DIM    = "#64748b"
TEXT_LIGHT  = "#cbd5e1"
TEXT_WHITE  = "#f8fafc"

KPI_COLORS  = ["#1e293b", "#14532d", "#7c2d12", "#3b0764"]
KPI_ACCENTS = ["#38bdf8", "#4ade80", "#fb923c", "#c084fc"]

DUR_COLORS  = ["#0ea5e9","#38bdf8","#7dd3fc","#bae6fd","#0369a1","#075985"]

STATUS_COLORS = {
    "Completed":    "#4c1d95",
    "Placed":       "#7c3aed",
    "Active":       "#a78bfa",
    "Discontinued": "#ddd6fe",
}

TASK_DONE_COLOR = "#22c55e"
TASK_NOT_COLOR  = "#ef4444"

#LOAD & CALCULATE DATA FROM EXCEL
df = pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME)

# Clean
df["status_clean"] = df["status(active/completed/placed)"].astype(str).str.strip()
df["Duration in months"] = pd.to_numeric(df["Duration in months"], errors="coerce")
df["Start date"] = pd.to_datetime(df["Start date"], errors="coerce")
df["year"] = df["Start date"].dt.year

# KPIs
total_interns       = len(df)
completed_count     = (df["status_clean"].str.lower() == "completed").sum()
discontinued_count  = (df["status_clean"].str.lower() == "discontinued").sum()
avg_duration        = df["Duration in months"].mean()

kpi_labels  = ["Total Interns", "Completed Interns", "Discontinued Interns", "Avg Duration (mo)"]
kpi_values  = [str(total_interns), str(completed_count), str(discontinued_count), f"{avg_duration:.3f}"]

# Duration breakdown
dur_counts = df["Duration in months"].value_counts().sort_index()
dur_labels = [f"{int(k)} month{'s' if k>1 else ''}" for k in dur_counts.index]
dur_values = dur_counts.values.tolist()

# Status counts
status_counts = df["status_clean"].value_counts()
status_order  = ["Completed", "Placed", "Active", "Discontinued"]
status_vals   = [int(status_counts.get(s, 0)) for s in status_order]

# Repeated interns
repeated = (
    df.groupby("Name")
      .size()
      .reset_index(name="cnt")
      .query("cnt > 1")
      .sort_values("Name")
)

# Progress by year
year_counts = df["year"].value_counts().sort_index().dropna()
year_labels = [str(int(y)) for y in year_counts.index]
year_values = year_counts.values.tolist()

# Top 10 colleges
college_counts = df["College Name"].value_counts().head(10)
college_names  = [n.split(",")[0][:26] for n in college_counts.index]   # shorten
college_values = college_counts.values.tolist()
top_college    = college_counts.index[0].split(",")[0][:26]

# Task completion
task_cols = [
    ("Orientation",                     "Orientation"),
    ("Personal data collection",        "Personal data collection"),
    ("Registration form filling",       "Registration form filling"),
    ("Tracking sheet creation",         "Tracking sheet creation"),
    ("Generate the certificate",        "Generate the certificate"),
    ("Provide cert & take photo",       "Provide certificate and take photo"),
]
task_data = []
for label, col in task_cols:
    if col in df.columns:
        done     = int((df[col] == 1).sum())
        not_done = int((df[col] == 0).sum())
        total    = done + not_done
        pct      = round(done / total * 100, 2) if total > 0 else 0
        task_data.append({"label": label, "done": done, "not_done": not_done,
                          "total": total, "pct": pct})

#HELPERS 
def draw_card(ax, color=CARD, border_color=BORDER, alpha=1.0):
    """Fill an axes background as a dark card."""
    ax.set_facecolor(color)
    for spine in ax.spines.values():
        spine.set_edgecolor(border_color)
        spine.set_linewidth(0.8)

def section_title(ax, title):
    ax.text(0.0, 1.02, title.upper(), transform=ax.transAxes,
            color=TEXT_DIM, fontsize=7, fontweight="bold", va="bottom")

def draw_treemap(ax, labels, values, colors):
    """Simple squarified-ish treemap drawn with rectangles."""
    total = sum(values)
    # Layout: big tile on left, smaller stacked on right
    rects = []
    # Sort descending
    items = sorted(zip(values, labels, colors), reverse=True)

    W, H = 1.0, 1.0
    GAP  = 0.012

    if len(items) == 0:
        return

    # First item takes left portion proportional to its share
    v0 = items[0][0]
    w0 = (v0 / total) * W - GAP / 2
    rects.append((0, 0, w0, H, items[0][1], items[0][2], items[0][0]))

    # Remaining items stacked on right
    x_start = w0 + GAP
    remaining = items[1:]
    rem_total = sum(r[0] for r in remaining)
    y = 0
    for val, lbl, clr in remaining:
        h = (val / rem_total) * H - GAP / 2 if rem_total > 0 else H
        rects.append((x_start, y, W - x_start, h, lbl, clr, val))
        y += h + GAP

    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")

    for (rx, ry, rw, rh, lbl, clr, val) in rects:
        patch = FancyBboxPatch((rx + 0.005, ry + 0.005),
                               rw - 0.010, rh - 0.010,
                               boxstyle="round,pad=0.01",
                               linewidth=0, facecolor=clr)
        ax.add_patch(patch)
        is_disc  = lbl == "Discontinued"
        txt_col  = "#1e1b4b" if is_disc else "white"
        cnt_col  = "#4c1d95" if is_disc else "#e9d5ff"
        fs_name  = max(7, min(11 if not is_disc else 8, rw * 18))
        fs_val   = max(6, fs_name - 1)
        cx, cy   = rx + rw / 2, ry + rh / 2
        if rw > 0.06 and rh > 0.08:
            ax.text(cx, cy + rh * 0.10, lbl, ha="center", va="center",
                    color=txt_col, fontsize=fs_name, fontweight="bold")
            ax.text(cx, cy - rh * 0.12, str(val), ha="center", va="center",
                    color=cnt_col, fontsize=fs_val, fontweight="bold")
        elif rw > 0.04:
            ax.text(cx, cy, f"{lbl}: {val}", ha="center", va="center",
                    color=txt_col, fontsize=max(6, fs_val - 1), fontweight="bold")


# FIGURE LAYOUT 
fig = plt.figure(figsize=(20, 13), facecolor=BG)
fig.subplots_adjust(left=0.03, right=0.97, top=0.93, bottom=0.06,
                    hspace=0.55, wspace=0.35)

# Title
fig.text(0.5, 0.965, "REPLICA OF INTERNSHIP MASTER",
         ha="center", color=TEXT_WHITE, fontsize=16, fontweight="bold",
         fontfamily="monospace")
fig.text(0.5, 0.948, "Intern Progress & Task Tracking Dashboard",
         ha="center", color=TEXT_DIM, fontsize=9)

# Gradient line under title (simulate with colored text underline)
line_ax = fig.add_axes([0.38, 0.940, 0.24, 0.003])
line_ax.set_facecolor("#7c3aed")
line_ax.axis("off")

# Main grid: 3 columns top, 1 wide middle, 6 small bottom
gs_top  = GridSpec(2, 3, figure=fig,
                   left=0.03, right=0.97, top=0.93, bottom=0.46,
                   hspace=0.5, wspace=0.3)
gs_mid  = GridSpec(1, 1, figure=fig,
                   left=0.03, right=0.97, top=0.435, bottom=0.27,
                   hspace=0.1)
gs_bot  = GridSpec(1, 6, figure=fig,
                   left=0.03, right=0.97, top=0.25, bottom=0.04,
                   hspace=0.1, wspace=0.4)

# ── KPI COLUMN (top-left, spans 2 rows as 4 sub-axes) ─────────────────────────
kpi_gs = GridSpec(4, 1, figure=fig,
                  left=0.03, right=0.215, top=0.93, bottom=0.46,
                  hspace=0.18)

for i, (lbl, val, bg, accent) in enumerate(
        zip(kpi_labels, kpi_values, KPI_COLORS, KPI_ACCENTS)):
    ax = fig.add_subplot(kpi_gs[i])
    ax.set_facecolor(bg)
    for spine in ax.spines.values():
        spine.set_edgecolor(accent)
        spine.set_linewidth(1.2)
    ax.set_xticks([]); ax.set_yticks([])
    ax.text(0.05, 0.78, lbl.upper(), transform=ax.transAxes,
            color=accent, fontsize=7, fontweight="bold", va="top")
    ax.text(0.05, 0.28, val, transform=ax.transAxes,
            color=TEXT_WHITE, fontsize=22, fontweight="bold",
            fontfamily="monospace", va="center")

# DURATION PIE (center-top-left) 
ax_dur = fig.add_subplot(gs_top[0, 1])
draw_card(ax_dur)
section_title(ax_dur, "Duration in Months")
wedges, texts, autotexts = ax_dur.pie(
    dur_values, labels=None,
    colors=DUR_COLORS[:len(dur_values)],
    autopct="%1.0f%%", startangle=90,
    pctdistance=0.75,
    wedgeprops=dict(linewidth=0.5, edgecolor=BG)
)
for at in autotexts:
    at.set_fontsize(7)
    at.set_color("white")
    at.set_fontweight("bold")
# Legend
legend_patches = [mpatches.Patch(color=DUR_COLORS[i], label=f"{dur_labels[i]}: {dur_values[i]}")
                  for i in range(len(dur_labels))]
ax_dur.legend(handles=legend_patches, loc="lower left",
              bbox_to_anchor=(-0.55, -0.05), fontsize=7,
              facecolor=CARD, edgecolor=BORDER, labelcolor=TEXT_LIGHT,
              framealpha=1, borderpad=0.6, handlelength=1)

# STATUS TREEMAP (center-top-right of row 1) 
ax_tree = fig.add_subplot(gs_top[1, 1])
draw_card(ax_tree)
section_title(ax_tree, "Status of Intern")
draw_treemap(ax_tree, status_order, status_vals,
             [STATUS_COLORS[s] for s in status_order])

#REPEATED INTERNSHIPS TABLE (right-top row 0) 
ax_rep = fig.add_subplot(gs_top[0, 2])
draw_card(ax_rep)
section_title(ax_rep, "Repeated Internships")
ax_rep.axis("off")

rep_names = repeated["Name"].tolist()
rep_cnts  = repeated["cnt"].tolist()

ax_rep.text(0.02, 0.97, "Name", color=TEXT_DIM, fontsize=7.5,
            fontweight="bold", transform=ax_rep.transAxes, va="top")
ax_rep.text(0.88, 0.97, "Ct", color=TEXT_DIM, fontsize=7.5,
            fontweight="bold", transform=ax_rep.transAxes, va="top", ha="right")

row_h = 0.085
for idx, (name, cnt) in enumerate(zip(rep_names, rep_cnts)):
    y = 0.88 - idx * row_h
    ax_rep.plot([0.02, 0.98], [y + row_h * 0.5, y + row_h * 0.5],
                color=BORDER, linewidth=0.4, transform=ax_rep.transAxes, clip_on=False)
    ax_rep.text(0.02, y, name, color=TEXT_LIGHT, fontsize=7.5,
                transform=ax_rep.transAxes, va="center")
    ax_rep.text(0.88, y, str(cnt), color="#a78bfa", fontsize=7.5,
                fontweight="bold", transform=ax_rep.transAxes,
                va="center", ha="right")

#PROGRESS LINE CHART (right-top row 1) 
ax_line = fig.add_subplot(gs_top[1, 2])
draw_card(ax_line)
section_title(ax_line, "Progress in Years")
ax_line.set_facecolor(CARD)
ax_line.plot(year_labels, year_values, color="#38bdf8",
             linewidth=2.5, marker="o", markersize=6,
             markerfacecolor="#38bdf8", markeredgecolor=BG, markeredgewidth=1.2)
ax_line.fill_between(year_labels, year_values, alpha=0.12, color="#38bdf8")
for x, y in zip(year_labels, year_values):
    ax_line.text(x, y + 8, str(y), ha="center", color="#38bdf8",
                 fontsize=8, fontweight="bold")
ax_line.set_facecolor(CARD)
ax_line.tick_params(colors=TEXT_DIM, labelsize=8)
ax_line.yaxis.label.set_color(TEXT_DIM)
ax_line.grid(True, color=BORDER, linewidth=0.5, linestyle="--", alpha=0.6)
for spine in ax_line.spines.values():
    spine.set_edgecolor(BORDER)
ax_line.set_ylim(0, max(year_values) * 1.2)

#COLLEGE BAR CHART (middle full-width) 
ax_bar = fig.add_subplot(gs_mid[0])
draw_card(ax_bar)
section_title(ax_bar, "College with Maximum Placement")
bar_colors = ["#7f1d1d" if n == top_college else "#fca5a5" for n in college_names]
bars = ax_bar.bar(college_names, college_values, color=bar_colors,
                  edgecolor=BG, linewidth=0.5, width=0.65)
for bar, val in zip(bars, college_values):
    ax_bar.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.5, str(val),
                ha="center", va="bottom", color=TEXT_LIGHT, fontsize=8, fontweight="bold")
ax_bar.set_facecolor(CARD)
ax_bar.tick_params(axis="x", colors=TEXT_DIM, labelsize=7.5, rotation=25)
ax_bar.tick_params(axis="y", colors=TEXT_DIM, labelsize=8)
ax_bar.grid(True, axis="y", color=BORDER, linewidth=0.5, linestyle="--", alpha=0.5)
for spine in ax_bar.spines.values():
    spine.set_edgecolor(BORDER)
ax_bar.set_ylim(0, max(college_values) * 1.18)

#TASK COMPLETION DONUTS (bottom row) 
for i, t in enumerate(task_data):
    ax_t = fig.add_subplot(gs_bot[0, i])
    ax_t.set_facecolor(CARD)
    for spine in ax_t.spines.values():
        spine.set_edgecolor(BORDER)

    # Donut
    wedge_vals  = [t["done"], t["not_done"]]
    wedge_clrs  = [TASK_DONE_COLOR, TASK_NOT_COLOR]
    wedges, _   = ax_t.pie(
        wedge_vals, colors=wedge_clrs,
        startangle=90,
        wedgeprops=dict(width=0.48, linewidth=0.8, edgecolor=BG)
    )

    # Centre text: pct, done count, not-done count
    ax_t.text(0, 0.18, f"{t['pct']:.1f}%",
              ha="center", va="center", color=TEXT_WHITE,
              fontsize=9, fontweight="bold")
    ax_t.text(0, -0.05, f"✓ {t['done']}",
              ha="center", va="center", color="#86efac", fontsize=8, fontweight="bold")
    ax_t.text(0, -0.28, f"✗ {t['not_done']}",
              ha="center", va="center", color="#fca5a5", fontsize=8, fontweight="bold")

    # Label below
    ax_t.set_title(t["label"], color=TEXT_DIM, fontsize=7.5,
                   pad=2, wrap=True)

# Bottom legend for tasks
fig.text(0.43, 0.025, "■", color=TASK_DONE_COLOR, fontsize=11)
fig.text(0.445, 0.025, "Done", color=TEXT_DIM, fontsize=8)
fig.text(0.49, 0.025, "■", color=TASK_NOT_COLOR, fontsize=11)
fig.text(0.505, 0.025, "Not Done", color=TEXT_DIM, fontsize=8)

# SAVE & SHOW 
OUTPUT = "internship_dashboard.png"
plt.savefig(OUTPUT, dpi=150, bbox_inches="tight", facecolor=BG)
print(f"Dashboard saved to: {OUTPUT}")
plt.show()

