"""
╔══════════════════════════════════════════════════════════╗
║        INTERNSHIP MASTER DASHBOARD GENERATOR            ║
║  Asks you for file path & column info, then builds      ║
║  the full dashboard automatically from your Excel.      ║
╚══════════════════════════════════════════════════════════╝

Requirements:
    pip install matplotlib pandas openpyxl

Usage:
    python internship_dashboard.py
"""

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings("ignore")

# ── COLORS ─────────────────────────────────────────────────────────────────────
BG            = "#0a0f1e"
CARD          = "#1e293b"
BORDER        = "#1e3a5f"
TEXT_DIM      = "#64748b"
TEXT_LIGHT    = "#cbd5e1"
TEXT_WHITE    = "#f8fafc"
KPI_COLORS    = ["#1e293b", "#14532d", "#7c2d12", "#3b0764"]
KPI_ACCENTS   = ["#38bdf8", "#4ade80", "#fb923c", "#c084fc"]
DUR_COLORS    = ["#0ea5e9","#38bdf8","#7dd3fc","#bae6fd","#0369a1","#075985"]
STATUS_COLORS = {
    "Completed":    "#4c1d95",
    "Placed":       "#7c3aed",
    "Active":       "#a78bfa",
    "Discontinued": "#ddd6fe",
}
TASK_DONE_COLOR = "#22c55e"
TASK_NOT_COLOR  = "#ef4444"

# ══════════════════════════════════════════════════════════════════════════════
#  HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def separator():
    print("\n" + "─" * 60)

def ask(prompt, default=None):
    suffix = f" [{default}]" if default else ""
    answer = input(f"  {prompt}{suffix}: ").strip()
    return answer if answer else default

def ask_column(df, prompt, default=None):
    while True:
        col = ask(prompt, default)
        if col and col in df.columns:
            return col
        close = [c for c in df.columns if col and col.lower() in c.lower()]
        print(f"\n  ⚠  Column '{col}' not found.")
        if close:
            print(f"     Did you mean: {close}")
        print(f"     Available: {list(df.columns)}\n")

def ask_task_columns(df):
    print("\n🔍 Auto-detecting task columns (0/1 values)...\n")

    task_cols = []

    for col in df.columns:
        unique_vals = set(df[col].dropna().unique())

        # Convert to set of integers safely
        try:
            unique_vals = set(int(v) for v in unique_vals)
        except:
            continue

        # Check if column only has 0/1
        if unique_vals.issubset({0, 1}) and len(unique_vals) > 0:
            task_cols.append(col)

    if not task_cols:
        print("⚠ No task columns detected automatically.")
    else:
        print(f"✅ Detected task columns: {task_cols}")

    return task_cols
    
def _guess(df, keywords):
    for kw in keywords:
        for col in df.columns:
            col_str = str(col)   
            if kw.lower() in col_str.lower():
                return col
    return None

def _find(values, keyword):
    for v in values:
        if keyword.lower() in str(v).lower():
            return v
    return values[0] if values else ""

# ══════════════════════════════════════════════════════════════════════════════
#  STEP 1 — COLLECT INPUTS
# ══════════════════════════════════════════════════════════════════════════════

def collect_inputs():
    print("\n")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║        INTERNSHIP MASTER DASHBOARD GENERATOR            ║")
    print("╚══════════════════════════════════════════════════════════╝")

    # FILE PATH
    separator()
    print("\n📂  STEP 1: Excel File Path")
    print("  Tip: Drag & drop your file into this window to get the path.\n")
    while True:
        path = ask("Full path to your Excel file (.xlsx)")
        if not path:
            print("  ⚠  Path cannot be empty."); continue
        path = path.strip('"').strip("'")
        if not os.path.exists(path):
            print(f"  ⚠  File not found at: {path}\n"); continue
        if not path.lower().endswith((".xlsx",".xls")):
            if ask("  Not an .xlsx file. Continue anyway? (yes/no)","no").lower() not in ("yes","y"):
                continue
        break

    # SHEET NAME
    separator()
    print("\n📋  STEP 2: Sheet Name")
    xl     = pd.ExcelFile(path)
    sheets = xl.sheet_names
    print(f"  Sheets found: {sheets}")
    while True:
        sheet = ask("Sheet name to use", sheets[0])
        if sheet in sheets:
            break
        print(f"  ⚠  '{sheet}' not found. Available: {sheets}")

    print(f"\n  Loading '{sheet}'...")
    df = pd.read_excel(path, sheet_name=sheet)
    print(f"  ✓ {len(df)} rows × {len(df.columns)} columns loaded.\n")

    # COLUMN MAPPING
    separator()
    print("\n🗂  STEP 3: Column Mapping\n")
    col_name     = ask_column(df, "Column for intern NAME",         _guess(df,["name","intern"]))
    col_college  = ask_column(df, "Column for COLLEGE NAME",        _guess(df,["college","institution","university"]))
    col_status   = ask_column(df, "Column for STATUS",              _guess(df,["status","active","completed"]))
    col_duration = ask_column(df, "Column for DURATION IN MONTHS",  _guess(df,["duration","months"]))
    col_start    = ask_column(df, "Column for START DATE",          _guess(df,["start","join","date"]))

    # STATUS LABELS
    separator()
    print("\n🏷  STEP 4: Status Labels")
    unique_statuses = df[col_status].dropna().astype(str).str.strip().unique().tolist()
    print(f"  Values found in status column: {unique_statuses}\n")
    label_completed    = ask("Which value means 'Completed'?",    _find(unique_statuses,"completed"))
    label_discontinued = ask("Which value means 'Discontinued'?", _find(unique_statuses,"discontinued"))

    # TASK COLUMNS
    separator()
    print("\n✅  STEP 5: Task Completion Columns (0/1 columns)\n")
    task_cols = ask_task_columns(df)

    # OUTPUT PATH
    separator()
    print("\n💾  STEP 6: Output File")
    default_out = os.path.join(os.path.dirname(os.path.abspath(path)), "internship_dashboard.png")
    out_path    = ask("Save dashboard image to", default_out)

    separator()
    print("\n  ✅  All inputs collected! Generating your dashboard...\n")

    return {
        "df": df, "path": path, "sheet": sheet,
        "col_name": col_name, "col_college": col_college,
        "col_status": col_status, "col_duration": col_duration,
        "col_start": col_start,
        "label_completed": label_completed, "label_discontinued": label_discontinued,
        "task_cols": task_cols, "out_path": out_path,
    }

# ══════════════════════════════════════════════════════════════════════════════
#  STEP 2 — CALCULATE METRICS
# ══════════════════════════════════════════════════════════════════════════════

def calculate_metrics(cfg):
    df = cfg["df"].copy()
    df["_status"]   = df[cfg["col_status"]].astype(str).str.strip()
    df["_duration"] = pd.to_numeric(df[cfg["col_duration"]], errors="coerce")
    df["_start"]    = pd.to_datetime(df[cfg["col_start"]], errors="coerce")
    df["_year"]     = df["_start"].dt.year
    df["_name"]     = df[cfg["col_name"]].astype(str).str.strip()
    df["_college"]  = df[cfg["col_college"]].astype(str).str.strip()

    lc = cfg["label_completed"].strip()
    ld = cfg["label_discontinued"].strip()

    # KPIs
    total       = len(df)
    completed_n = (df["_status"] == lc).sum()
    disc_n      = (df["_status"] == ld).sum()
    avg_dur     = df["_duration"].mean()

    # Duration
    dur_vc  = df["_duration"].value_counts().sort_index().dropna()
    dur_lbl = [f"{int(k)} month{'s' if k>1 else ''}" for k in dur_vc.index]
    dur_val = dur_vc.values.tolist()

    # Status treemap
    status_vc    = df["_status"].value_counts()
    fixed_order  = [lc, "Placed", "Active", ld]
    extras       = [s for s in status_vc.index if s not in fixed_order]
    status_order = [s for s in fixed_order if s in status_vc.index] + extras
    status_vals  = [int(status_vc.get(s, 0)) for s in status_order]
    extra_colors = ["#6d28d9","#8b5cf6","#c4b5fd","#ede9fe"]
    s_colors     = [STATUS_COLORS.get(s, extra_colors[i % 4])
                    for i, s in enumerate(status_order)]

    # Repeated
    repeated = (df.groupby("_name").size()
                  .reset_index(name="cnt")
                  .query("cnt > 1")
                  .sort_values("_name"))

    # Year progress
    yr_vc  = df["_year"].value_counts().sort_index().dropna()
    yr_lbl = [str(int(y)) for y in yr_vc.index]
    yr_val = yr_vc.values.tolist()

    # Colleges
    col_vc    = df["_college"].value_counts().head(10)
    col_names = [n.split(",")[0][:26] for n in col_vc.index]
    col_vals  = col_vc.values.tolist()
    top_col   = col_names[0] if col_names else ""

    # Tasks
    task_data = []
    for col in cfg["task_cols"]:
        done     = int((df[col] == 1).sum())
        not_done = int((df[col] == 0).sum())
        total_t  = done + not_done
        pct      = round(done / total_t * 100, 2) if total_t > 0 else 0
        label    = col if len(col) <= 28 else col[:26] + "…"
        task_data.append({"label": label, "done": done,
                           "not_done": not_done, "total": total_t, "pct": pct})

    return {
        "total": total, "completed_n": completed_n,
        "disc_n": disc_n, "avg_dur": avg_dur,
        "dur_lbl": dur_lbl, "dur_val": dur_val,
        "status_order": status_order, "status_vals": status_vals, "s_colors": s_colors,
        "repeated": repeated,
        "yr_lbl": yr_lbl, "yr_val": yr_val,
        "col_names": col_names, "col_vals": col_vals, "top_col": top_col,
        "task_data": task_data,
    }

# ══════════════════════════════════════════════════════════════════════════════
#  STEP 3 — DRAW DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════

def draw_card(ax):
    ax.set_facecolor(CARD)
    for sp in ax.spines.values():
        sp.set_edgecolor(BORDER); sp.set_linewidth(0.8)

def section_title(ax, title):
    ax.text(0.0, 1.02, title.upper(), transform=ax.transAxes,
            color=TEXT_DIM, fontsize=7, fontweight="bold", va="bottom")

def draw_treemap(ax, labels, values, colors):
    total = sum(values)
    if total == 0: return
    items   = sorted(zip(values, labels, colors), reverse=True)
    W,H,G   = 1.0, 1.0, 0.012
    v0      = items[0][0]
    w0      = (v0/total)*W - G/2
    rects   = [(0, 0, w0, H, items[0][1], items[0][2], items[0][0])]
    x0      = w0 + G
    rem     = items[1:]
    rem_tot = sum(r[0] for r in rem)
    y = 0
    for val, lbl, clr in rem:
        h = (val/rem_tot)*H - G/2 if rem_tot > 0 else H
        rects.append((x0, y, W-x0, h, lbl, clr, val))
        y += h + G
    ax.set_xlim(0,W); ax.set_ylim(0,H); ax.axis("off")
    for (rx,ry,rw,rh,lbl,clr,val) in rects:
        ax.add_patch(FancyBboxPatch((rx+.005,ry+.005), rw-.010, rh-.010,
                                    boxstyle="round,pad=0.01", linewidth=0, facecolor=clr))
        is_d = lbl == "Discontinued"
        tc   = "#1e1b4b" if is_d else "white"
        sc   = "#4c1d95" if is_d else "#e9d5ff"
        fsn  = max(7, min(8 if is_d else 11, rw*18))
        fsv  = max(6, fsn-1)
        cx,cy = rx+rw/2, ry+rh/2
        if rw > 0.06 and rh > 0.08:
            ax.text(cx, cy+rh*.10, lbl,    ha="center", va="center", color=tc, fontsize=fsn, fontweight="bold")
            ax.text(cx, cy-rh*.12, str(val),ha="center", va="center", color=sc, fontsize=fsv, fontweight="bold")
        elif rw > 0.04:
            ax.text(cx, cy, f"{lbl}: {val}", ha="center", va="center", color=tc, fontsize=max(6,fsv-1), fontweight="bold")

def build_dashboard(cfg, m):
    n_tasks = len(m["task_data"])
    max_tasks = max(1, min(n_tasks, 6))  # 🔥 never 0

    fig = plt.figure(figsize=(22, 17), facecolor=BG)

    # Title
    fig.text(0.5, 0.965, "INTERNSHIP MASTER DASHBOARD",
             ha="center", color=TEXT_WHITE, fontsize=16, fontweight="bold", fontfamily="monospace")
    fig.text(0.5, 0.948,
             f"File: {os.path.basename(cfg['path'])}  |  Sheet: {cfg['sheet']}  |  Records: {m['total']}",
             ha="center", color=TEXT_DIM, fontsize=8.5)

    la = fig.add_axes([0.36, 0.940, 0.28, 0.003])
    la.set_facecolor("#7c3aed")
    la.axis("off")

    # Layouts
    gs_top = GridSpec(2, 3, figure=fig, left=0.03, right=0.97, top=0.93, bottom=0.50, hspace=0.55, wspace=0.32)
    gs_mid = GridSpec(1, 1, figure=fig, left=0.03, right=0.97, top=0.47, bottom=0.30)

    # 🔥 Fixed bottom layout
    gs_bot = GridSpec(
        1, max_tasks,
        figure=fig,
        left=0.05,
        right=0.95,
        top=0.28,
        bottom=0.06,
        wspace=0.5
    )

    kpi_gs = GridSpec(4, 1, figure=fig, left=0.03, right=0.215, top=0.93, bottom=0.50, hspace=0.18)

    # KPI Cards
    kpi_labels = ["Total Interns","Completed Interns","Discontinued Interns","Avg Duration (mo)"]
    kpi_values = [str(m["total"]), str(m["completed_n"]), str(m["disc_n"]), f"{m['avg_dur']:.3f}"]

    for i,(lbl,val,bg,acc) in enumerate(zip(kpi_labels,kpi_values,KPI_COLORS,KPI_ACCENTS)):
        ax = fig.add_subplot(kpi_gs[i])
        ax.set_facecolor(bg)
        for sp in ax.spines.values():
            sp.set_edgecolor(acc)
            sp.set_linewidth(1.2)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.text(0.05,0.78, lbl.upper(), transform=ax.transAxes, color=acc, fontsize=7, fontweight="bold")
        ax.text(0.05,0.28, val, transform=ax.transAxes, color=TEXT_WHITE, fontsize=22,
                fontweight="bold", fontfamily="monospace")

    # Duration Pie
    ax_dur = fig.add_subplot(gs_top[0,1])
    draw_card(ax_dur)
    section_title(ax_dur,"Duration in Months")

    clrs = DUR_COLORS[:len(m["dur_val"])]
    _,_,ats = ax_dur.pie(m["dur_val"], colors=clrs, autopct="%1.0f%%", startangle=90,
                        pctdistance=0.75, wedgeprops=dict(linewidth=0.5,edgecolor=BG))

    for at in ats:
        at.set_fontsize(7)
        at.set_color("white")
        at.set_fontweight("bold")

    # Status Treemap
    ax_tree = fig.add_subplot(gs_top[1,1])
    draw_card(ax_tree)
    section_title(ax_tree,"Status of Intern")
    draw_treemap(ax_tree, m["status_order"], m["status_vals"], m["s_colors"])

    # College Bar
    ax_bar = fig.add_subplot(gs_mid[0])
    draw_card(ax_bar)
    section_title(ax_bar,"College with Maximum Placement")

    bar_colors = ["#7f1d1d" if n==m["top_col"] else "#fca5a5" for n in m["col_names"]]
    bars = ax_bar.bar(m["col_names"], m["col_vals"], color=bar_colors)

    for bar,val in zip(bars,m["col_vals"]):
        ax_bar.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5, str(val),
                    ha="center", color=TEXT_LIGHT, fontsize=8)

    ax_bar.tick_params(axis="x", rotation=35)

    # 🔥 SAFE DONUT SECTION
    if n_tasks == 0:
        ax_t = fig.add_subplot(gs_bot[0, 0])
        ax_t.set_facecolor(CARD)
        ax_t.text(0.5, 0.5, "No Task Data Selected",
                  ha="center", va="center",
                  color=TEXT_DIM, fontsize=12)
        ax_t.axis("off")
    else:
        for i, t in enumerate(m["task_data"][:max_tasks]):
            ax_t = fig.add_subplot(gs_bot[0, i])
            ax_t.set_facecolor(CARD)

            for sp in ax_t.spines.values():
                sp.set_edgecolor(BORDER)

            ax_t.pie(
                [t["done"], t["not_done"]],
                colors=[TASK_DONE_COLOR, TASK_NOT_COLOR],
                startangle=90,
                wedgeprops=dict(width=0.55, linewidth=1, edgecolor=BG)
            )

            ax_t.text(0, 0.2, f"{t['pct']:.1f}%", ha="center",
                      color=TEXT_WHITE, fontsize=11, fontweight="bold")

            ax_t.text(0, -0.05, f"✓ {t['done']}", ha="center",
                      color="#86efac", fontsize=9, fontweight="bold")

            ax_t.text(0, -0.30, f"✗ {t['not_done']}", ha="center",
                      color="#fca5a5", fontsize=9, fontweight="bold")

            ax_t.set_title(t["label"], color=TEXT_DIM, fontsize=9, pad=10)

    # Legend
    fig.text(0.43,0.04,"■",color=TASK_DONE_COLOR,fontsize=11)
    fig.text(0.445,0.04,"Done",color=TEXT_DIM,fontsize=9)
    fig.text(0.49,0.04,"■",color=TASK_NOT_COLOR,fontsize=11)
    fig.text(0.505,0.04,"Not Done",color=TEXT_DIM,fontsize=9)

    plt.savefig(cfg["out_path"], dpi=150, bbox_inches="tight", facecolor=BG)
    print(f"\n  ✅ Dashboard saved → {cfg['out_path']}\n")

    plt.show()

    # Save
    plt.savefig(cfg["out_path"], dpi=150, bbox_inches="tight", facecolor=BG)
    print(f"\n  ✅  Dashboard saved → {cfg['out_path']}\n")
    plt.show()

# ══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        cfg     = collect_inputs()
        metrics = calculate_metrics(cfg)
        build_dashboard(cfg, metrics)
    except KeyboardInterrupt:
        print("\n\n  Cancelled. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n  ❌  Error: {e}")
        raise