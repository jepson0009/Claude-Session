import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np

fig, ax = plt.subplots(figsize=(12, 9))
fig.patch.set_facecolor("white")
ax.set_facecolor("#F9FAFB")

# ── Axes setup ────────────────────────────────────────────────────────────────
ax.set_xlim(-1.15, 1.15)
ax.set_ylim(-1.15, 1.15)
ax.axhline(0, color="#D1D5DB", lw=1.2, zorder=1)
ax.axvline(0, color="#D1D5DB", lw=1.2, zorder=1)
ax.spines[["top","right","left","bottom"]].set_visible(False)
ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

# Quadrant shading
for (x0, y0, w, h, c) in [
    (-1.15, 0,    1.15, 1.15, "#EFF6FF"),   # top-left:  PM + Premium
    (0,     0,    1.15, 1.15, "#F0FDF4"),   # top-right: Agentic + Premium
    (-1.15, -1.15,1.15, 1.15, "#FEF9C3"),   # bot-left:  PM + Bundled
    (0,     -1.15,1.15, 1.15, "#FFF1F2"),   # bot-right: Agentic + Bundled
]:
    ax.add_patch(plt.Rectangle((x0, y0), w, h, color=c, zorder=0))

# Quadrant labels (corner text)
quad_labels = [
    (-1.12,  1.10, "PM-centric\n+ Premium add-on",  "#1D4ED8"),
    ( 0.03,  1.10, "Agentic\n+ Premium add-on",      "#15803D"),
    (-1.12, -1.12, "PM-centric\n+ Bundled",          "#92400E"),
    ( 0.03, -1.12, "Agentic\n+ Bundled",             "#9F1239"),
]
for x, y, txt, col in quad_labels:
    ax.text(x, y, txt, fontsize=8, color=col, va="top", ha="left",
            fontstyle="italic", alpha=0.75)

# ── Competitor positions ──────────────────────────────────────────────────────
# (x=agentic score, y=premium score, label, color, marker)
players = [
    ( 0.62, -0.60, "Asana",              "#F97316", "o"),
    ( 0.48, -0.72, "Monday.com",         "#8B5CF6", "s"),
    ( 0.88,  0.70, "Atlassian",          "#0EA5E9", "D"),
    (-0.68,  0.52, "Smartsheet",         "#6B7280", "^"),
    (-0.22,  0.62, "Meridian\n(today)",  "#DC2626", "o"),
    ( 0.70,  0.55, "Meridian\n(Option B)","#16A34A","*"),
]

for x, y, label, color, marker in players:
    ms = 220 if marker == "*" else 130
    ax.scatter(x, y, s=ms, color=color, marker=marker,
               zorder=5, edgecolors="white", linewidths=1.5)

# Arrow: Meridian today → Option B
ax.annotate("",
    xy=(0.70, 0.55), xytext=(-0.22, 0.62),
    arrowprops=dict(arrowstyle="-|>", color="#DC2626",
                    lw=2.0, connectionstyle="arc3,rad=-0.25"),
    zorder=4)

# Labels with offsets tuned to avoid overlap
label_offsets = {
    "Asana":              ( 0.07, -0.09),
    "Monday.com":         (-0.18, -0.09),
    "Atlassian":          ( 0.07,  0.07),
    "Smartsheet":         (-0.18,  0.07),
    "Meridian\n(today)":  (-0.26,  0.05),
    "Meridian\n(Option B)":( 0.07,  0.06),
}
for x, y, label, color, marker in players:
    dx, dy = label_offsets[label]
    weight = "bold" if "Meridian" in label else "normal"
    ax.text(x + dx, y + dy, label, fontsize=9.5, color=color,
            fontweight=weight, va="center", ha="left", zorder=6,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.7))

# ── Axis arrows and labels ────────────────────────────────────────────────────
arrow_kw = dict(arrowstyle="-|>", color="#374151", lw=1.5)
ax.annotate("", xy=( 1.12, 0), xytext=(-1.12, 0),
            arrowprops=arrow_kw)
ax.annotate("", xy=(-1.12, 0), xytext=( 1.12, 0),
            arrowprops=arrow_kw)
ax.annotate("", xy=(0,  1.12), xytext=(0, -1.12),
            arrowprops=arrow_kw)
ax.annotate("", xy=(0, -1.12), xytext=(0,  1.12),
            arrowprops=arrow_kw)

ax.text( 1.13,  0.04, "Agentic →",    fontsize=10, fontweight="bold",
         color="#374151", ha="right", va="bottom")
ax.text(-1.13,  0.04, "← PM-centric", fontsize=10, fontweight="bold",
         color="#374151", ha="left", va="bottom")
ax.text( 0.03,  1.13, "Premium / Add-on pricing →", fontsize=10,
         fontweight="bold", color="#374151", va="top", ha="left")
ax.text( 0.03, -1.13, "← Bundled pricing", fontsize=10,
         fontweight="bold", color="#374151", va="bottom", ha="left")

# ── Annotation callouts ───────────────────────────────────────────────────────
callouts = [
    # (text, xy_point, xy_text, color)
    ("Agent OS; AI Studio\nbundled in Adv+ tiers",
     (0.62, -0.60), (0.40, -0.90), "#F97316"),
    ("Work OS; monday AI Agents\nbundled in Pro+",
     (0.48, -0.72), (0.05, -1.02), "#8B5CF6"),
    ("Rovo Studio; separate\npaid product + consumption",
     (0.88,  0.70), (0.60,  1.00), "#0EA5E9"),
    ('"Trust-first" AI; compliance\nadd-on; slowing growth',
     (-0.68, 0.52), (-1.10, 0.88), "#6B7280"),
]
for txt, xy, xytext, color in callouts:
    ax.annotate(txt, xy=xy, xytext=xytext,
                fontsize=7.5, color=color, ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.3", fc="white",
                          ec=color, alpha=0.9, lw=0.8),
                arrowprops=dict(arrowstyle="-", color=color,
                                lw=0.8, alpha=0.6),
                zorder=7)

# White-space box
ax.text(0.70, 0.08,
        "White space:\nEnterprise-governed\nagentic work\n(regulated industries)",
        fontsize=8, color="#15803D", ha="center", va="center",
        bbox=dict(boxstyle="round,pad=0.4", fc="#DCFCE7",
                  ec="#16A34A", lw=1.2, alpha=0.9),
        zorder=7)

# ── Title and caption ─────────────────────────────────────────────────────────
ax.set_title(
    "Competitive Positioning Matrix — AI Strategy\n"
    "Meridian Technologies  ·  Investor Day Prep  ·  Feb 2026",
    fontsize=13, fontweight="bold", pad=14, color="#111827")

fig.text(0.5, 0.01,
    "Sources: competitors_cached/ (Asana, Monday, Atlassian, Smartsheet)  ·  "
    "meridian_ai_strategy_options.md  ·  meridian_recent_customer_feedback.md",
    ha="center", fontsize=7.5, color="#9CA3AF")

plt.tight_layout(rect=[0, 0.03, 1, 1])
plt.savefig("positioning_matrix.png", dpi=150, bbox_inches="tight")
print("Saved: positioning_matrix.png")
