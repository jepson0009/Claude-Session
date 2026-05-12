import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import numpy as np

# ── Colours ───────────────────────────────────────────────────────────────────
C = {
    "meridian":   "#16A34A",
    "asana":      "#F97316",
    "monday":     "#8B5CF6",
    "atlassian":  "#0EA5E9",
    "smartsheet": "#6B7280",
    "bg":         "#0F172A",      # slide dark background
    "panel":      "#1E293B",      # panel background
    "grid":       "#334155",      # grid lines
    "text":       "#F1F5F9",      # primary text
    "muted":      "#94A3B8",      # secondary text
    "accent":     "#38BDF8",      # highlight
    "green_bg":   "#14532D",      # white-space callout
    "green_bd":   "#22C55E",
}

# ── Figure / layout ───────────────────────────────────────────────────────────
fig = plt.figure(figsize=(16, 10), facecolor=C["bg"])
gs  = GridSpec(2, 2, figure=fig,
               left=0.04, right=0.98, top=0.88, bottom=0.04,
               wspace=0.06, hspace=0.06,
               width_ratios=[1.55, 1], height_ratios=[1, 0.48])

ax_map   = fig.add_subplot(gs[:, 0])   # 2×2 matrix (full left column)
ax_table = fig.add_subplot(gs[0, 1])   # capability table (top-right)
ax_key   = fig.add_subplot(gs[1, 1])   # takeaway box (bottom-right)

for ax in [ax_map, ax_table, ax_key]:
    ax.set_facecolor(C["panel"])
    ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
    for spine in ax.spines.values():
        spine.set_edgecolor(C["grid"])

# ══════════════════════════════════════════════════════════════════════════════
# LEFT — 2×2 matrix
# ══════════════════════════════════════════════════════════════════════════════
ax = ax_map
ax.set_xlim(-1.15, 1.15)
ax.set_ylim(-1.15, 1.15)

# Quadrant fills
fills = [
    (-1.15, 0,     1.15, 1.15, "#1E3A5F22"),  # top-left:  gov+, low agentic
    (0,     0,     1.15, 1.15, "#14532D33"),  # top-right: gov+, agentic  ← target
    (-1.15, -1.15, 1.15, 1.15, "#1E293B"),    # bot-left:  low both
    (0,     -1.15, 1.15, 1.15, "#3B0764aa"),  # bot-right: agentic, low gov
]
for x0, y0, w, h, col in fills:
    ax.add_patch(plt.Rectangle((x0, y0), w, h, color=col, zorder=0))

ax.axhline(0, color=C["grid"], lw=1.0, zorder=1)
ax.axvline(0, color=C["grid"], lw=1.0, zorder=1)

# Quadrant watermarks
qw = [
    (-0.58,  0.85, "HIGH GOVERNANCE\nLOW AGENTIC",  C["accent"],   0.20),
    ( 0.42,  0.85, "HIGH GOVERNANCE\nHIGH AGENTIC", C["green_bd"], 0.30),
    (-0.58, -0.85, "LOW GOVERNANCE\nLOW AGENTIC",   C["muted"],    0.15),
    ( 0.42, -0.85, "LOW GOVERNANCE\nHIGH AGENTIC",  "#A855F7",     0.20),
]
for x, y, txt, col, alpha in qw:
    ax.text(x, y, txt, ha="center", va="center", fontsize=7.5,
            color=col, alpha=alpha, fontweight="bold", linespacing=1.6,
            transform=ax.transData, zorder=1)

# White-space callout (top-right quadrant)
ax.add_patch(plt.Rectangle((0.02, 0.02), 1.11, 1.11,
             fill=False, edgecolor=C["green_bd"], lw=1.5,
             linestyle="--", zorder=2, alpha=0.6))
ax.text(0.575, 0.12, "TARGET\nWHITE SPACE",
        ha="center", va="bottom", fontsize=7, color=C["green_bd"],
        fontweight="bold", alpha=0.7, zorder=3)

# ── Player positions ──────────────────────────────────────────────────────────
# (x=agentic, y=governance, label, color, marker, label_offset)
players = [
    ( 0.72,  0.72, "Meridian\n(Option B)", C["meridian"],   "*",  ( 0.09,  0.05)),
    (-0.20,  0.55, "Meridian\n(today)",    C["meridian"],   "o",  (-0.32,  0.06)),
    ( 0.60, -0.45, "Asana",               C["asana"],      "o",  ( 0.09, -0.06)),
    ( 0.42, -0.62, "Monday.com",          C["monday"],     "s",  ( 0.09, -0.06)),
    ( 0.82,  0.40, "Atlassian",           C["atlassian"],  "D",  ( 0.09,  0.05)),
    (-0.65,  0.50, "Smartsheet",          C["smartsheet"], "^",  (-0.30,  0.06)),
]

# Arrow Meridian today → Option B
ax.annotate("",
    xy=(0.72, 0.72), xytext=(-0.20, 0.55),
    arrowprops=dict(arrowstyle="-|>", color=C["meridian"],
                    lw=2.2, connectionstyle="arc3,rad=-0.30"),
    zorder=4)

for x, y, label, color, marker, (dx, dy) in players:
    ms = 280 if marker == "*" else 140
    ax.scatter(x, y, s=ms, color=color, marker=marker,
               edgecolors="white", linewidths=1.2, zorder=5)
    weight = "bold" if "Meridian" in label else "normal"
    ax.text(x + dx, y + dy, label,
            fontsize=9, color=color, fontweight=weight,
            va="center", ha="left", zorder=6,
            bbox=dict(boxstyle="round,pad=0.25", fc=C["panel"],
                      ec="none", alpha=0.85))

# Axis arrows + labels
for xy, xt in [((1.13,0),(-1.13,0)), ((0,1.13),(0,-1.13))]:
    ax.annotate("", xy=xy, xytext=xt,
                arrowprops=dict(arrowstyle="-|>", color=C["muted"], lw=1.2))

ax.text( 1.14,  0.05, "Agentic Commitment →",
         fontsize=9, color=C["text"], fontweight="bold", ha="right", va="bottom")
ax.text(-1.14,  0.05, "← Low Agentic",
         fontsize=8, color=C["muted"], ha="left", va="bottom")
ax.text( 0.03,  1.14, "Governance Depth →",
         fontsize=9, color=C["text"], fontweight="bold", va="top", ha="left")
ax.text( 0.03, -1.14, "← Low Governance",
         fontsize=8, color=C["muted"], va="bottom", ha="left")

ax.set_title("Governance Depth  vs.  Agentic Commitment",
             fontsize=11, color=C["text"], pad=10, fontweight="bold")

# ══════════════════════════════════════════════════════════════════════════════
# TOP-RIGHT — Capability comparison table
# ══════════════════════════════════════════════════════════════════════════════
ax = ax_table
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

ax.text(0.5, 0.97, "Capability Comparison",
        ha="center", va="top", fontsize=10.5, fontweight="bold",
        color=C["text"])

# Column headers
cols  = ["Meridian", "Asana", "Monday", "Atlassian", "Smartsheet"]
col_x = [0.22, 0.38, 0.52, 0.67, 0.84]
col_c = [C["meridian"], C["asana"], C["monday"], C["atlassian"], C["smartsheet"]]
header_y = 0.88

for label, x, col in zip(cols, col_x, col_c):
    ax.text(x, header_y, label, ha="center", va="top",
            fontsize=8, fontweight="bold", color=col)

ax.plot([0.02, 0.98], [0.83, 0.83],
        color=C["grid"], lw=0.8, transform=ax.transAxes, clip_on=False)

# Rows: (capability label, [Meridian, Asana, Monday, Atlassian, Smartsheet])
# ✦ = strong  ◑ = partial  ✗ = weak/none
STRONG  = ("✦", C["green_bd"])
PARTIAL = ("◑", "#FCD34D")
WEAK    = ("✗", "#F87171")

rows = [
    ("FedRAMP / HIPAA",           [STRONG,  WEAK,    WEAK,    PARTIAL, PARTIAL]),
    ("Agent audit logs",           [STRONG,  WEAK,    WEAK,    PARTIAL, STRONG ]),
    ("Role-based agent perms",     [STRONG,  WEAK,    WEAK,    PARTIAL, STRONG ]),
    ("Model selection / BYO",      [STRONG,  PARTIAL, PARTIAL, PARTIAL, STRONG ]),
    ("Data residency (EMEA)",      [STRONG,  PARTIAL, PARTIAL, STRONG,  PARTIAL]),
    ("Agentic product shipped",    [PARTIAL, STRONG,  STRONG,  STRONG,  WEAK   ]),
    ("Agent builder for customers",[PARTIAL, PARTIAL, STRONG,  STRONG,  WEAK   ]),
    ("Consumption pricing",        [PARTIAL, WEAK,    WEAK,    STRONG,  WEAK   ]),
    ("Regulated-industry verticals",[STRONG, WEAK,    WEAK,    PARTIAL, PARTIAL]),
    ("AI bundled in std tier",     [WEAK,    STRONG,  STRONG,  WEAK,    PARTIAL]),
]

row_start_y = 0.80
row_h       = 0.073

for i, (label, vals) in enumerate(rows):
    y = row_start_y - i * row_h
    bg = "#FFFFFF08" if i % 2 == 0 else "#00000000"
    ax.add_patch(plt.Rectangle((0.01, y - row_h*0.5), 0.98, row_h,
                                color=bg, zorder=0, transform=ax.transAxes,
                                clip_on=False))
    ax.text(0.02, y, label, ha="left", va="center",
            fontsize=7.5, color=C["muted"])
    for (sym, col), x in zip(vals, col_x):
        ax.text(x, y, sym, ha="center", va="center",
                fontsize=9, color=col, fontweight="bold")

# Legend
ly = 0.02
for sym, col, lbl in [(STRONG[0], STRONG[1], "Strong"),
                       (PARTIAL[0], PARTIAL[1], "Partial"),
                       (WEAK[0],   WEAK[1],   "Weak / none")]:
    ax.text(0.02, ly, sym, ha="left", va="bottom",
            fontsize=8, color=col, fontweight="bold")
    ax.text(0.07, ly, lbl, ha="left", va="bottom",
            fontsize=7, color=C["muted"])
    ly_next = 0.02
ax.text(0.35, 0.02, "◑ = Partial", fontsize=7, color=PARTIAL[1], va="bottom")
ax.text(0.02, 0.02, "✦ = Strong", fontsize=7, color=STRONG[1], va="bottom")
ax.text(0.60, 0.02, "✗ = Weak/none", fontsize=7, color=WEAK[1], va="bottom")

# ══════════════════════════════════════════════════════════════════════════════
# BOTTOM-RIGHT — Strategic takeaway
# ══════════════════════════════════════════════════════════════════════════════
ax = ax_key
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

ax.add_patch(plt.Rectangle((0.01, 0.04), 0.98, 0.92,
             color="#14532D", alpha=0.4, zorder=0,
             transform=ax.transAxes, clip_on=False))
ax.add_patch(plt.Rectangle((0.01, 0.04), 0.98, 0.92,
             fill=False, edgecolor=C["green_bd"], lw=1.0,
             transform=ax.transAxes, clip_on=False))

ax.text(0.5, 0.91, "Strategic Insight",
        ha="center", va="top", fontsize=9.5, fontweight="bold",
        color=C["green_bd"])

takeaway = (
    "No competitor combines high agentic commitment\n"
    "with deep enterprise governance.\n\n"
    "Atlassian is closest — but only for developer orgs.\n"
    "Asana & Monday are agentic but governance-light.\n"
    "Smartsheet has governance but rejected 'agentic.'\n\n"
    "Meridian's Option B targets the empty top-right:\n"
    "governed agentic work for regulated enterprises."
)
ax.text(0.5, 0.72, takeaway,
        ha="center", va="top", fontsize=8.5, color=C["text"],
        linespacing=1.65)

# ── Slide title ───────────────────────────────────────────────────────────────
fig.text(0.5, 0.955,
         "Competitive Positioning  —  Governance Depth vs. Agentic Commitment",
         ha="center", va="top", fontsize=14, fontweight="bold", color=C["text"])
fig.text(0.5, 0.928,
         "Meridian Technologies  ·  Investor Day Prep  ·  February 2026  ·  CONFIDENTIAL",
         ha="center", va="top", fontsize=8.5, color=C["muted"])

plt.savefig("competitive_positioning_slide.png", dpi=150,
            bbox_inches="tight", facecolor=C["bg"])
print("Saved: competitive_positioning_slide.png")
