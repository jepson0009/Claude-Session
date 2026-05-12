import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import textwrap

# ── Palette ───────────────────────────────────────────────────────────────────
C = {
    "bg":         "#0F172A",
    "panel":      "#1E293B",
    "border":     "#334155",
    "header_bg":  "#0EA5E9",
    "row_alt":    "#263348",
    "text":       "#F1F5F9",
    "muted":      "#94A3B8",
    "asana":      "#F97316",
    "monday":     "#8B5CF6",
    "atlassian":  "#0EA5E9",
    "smartsheet": "#94A3B8",
    "opt_a":      "#F59E0B",
    "opt_b":      "#22C55E",
}

# ── Table data ────────────────────────────────────────────────────────────────
columns = ["Competitor", "AI Positioning", "Pricing Posture",
           "Latest Flagship Announcement", "Closer to\nMeridian Option"]

rows = [
    {
        "name": "Asana",
        "color": C["asana"],
        "ai_pos": (
            "\"Agent Operating System\" — positions agents as the\n"
            "primary product; PM is the delivery surface.\n"
            "Brand: AI Studio + Smart Workflows."
        ),
        "pricing": (
            "Bundled: AI Studio included in\n"
            "Advanced & Enterprise tiers.\n"
            "No consumption pricing."
        ),
        "flagship": (
            "Nov 2025: Bundled AI Studio into\n"
            "Advanced+ tiers at no extra cost.\n"
            "Direct shot at add-on competitors."
        ),
        "option": "B",
        "option_note": "Agentic posture;\nno governance depth",
    },
    {
        "name": "Monday.com",
        "color": C["monday"],
        "ai_pos": (
            "\"Work OS supercharged with AI\" — AI is a layer\n"
            "across every product surface. Brand: monday AI,\n"
            "monday AI Workflows, monday AI Insights."
        ),
        "pricing": (
            "Bundled: monday AI Agents in\n"
            "Pro tier and above at no cost.\n"
            "No consumption pricing."
        ),
        "flagship": (
            "Jan 2026: GA of monday AI Agents —\n"
            "customer-buildable agents in natural\n"
            "language. Escalated bundling norm."
        ),
        "option": "B",
        "option_note": "Agentic direction;\nbreadth over depth",
    },
    {
        "name": "Atlassian",
        "color": C["atlassian"],
        "ai_pos": (
            "\"Agentic enterprise platform for software & IT\" —\n"
            "most explicit agentic pivot of the four. CEO:\n"
            "\"agent revenue > product revenue by 2028.\""
        ),
        "pricing": (
            "Hybrid: existing products per-seat;\n"
            "Rovo = per-seat + consumption.\n"
            "Only major player with consumption."
        ),
        "flagship": (
            "Jan 2026: Rovo Studio — dev-targeted\n"
            "agent builder, sold as separate\n"
            "premium SKU with consumption billing."
        ),
        "option": "B",
        "option_note": "Closest to Option B;\ngov only for dev orgs",
    },
    {
        "name": "Smartsheet",
        "color": C["smartsheet"],
        "ai_pos": (
            "\"Enterprise work platform you can trust with AI\" —\n"
            "explicitly rejected \"agentic\" label. Prefers\n"
            "\"AI-augmented.\" Trust-first, compliance-led."
        ),
        "pricing": (
            "Mixed: Smartsheet AI bundled in\n"
            "Business+; AI Compliance Pack is\n"
            "premium add-on (~$15/seat/mo)."
        ),
        "flagship": (
            "Dec 2025: AI Compliance Pack —\n"
            "agent audit logs, model selection,\n"
            "data residency for regulated cos."
        ),
        "option": "A",
        "option_note": "PM + trust framing;\nslowing growth",
    },
]

# ── Figure ────────────────────────────────────────────────────────────────────
ROW_H   = 0.185      # fraction of axes height per data row
HDR_H   = 0.075
PAD     = 0.012
n_rows  = len(rows)
fig_h   = 9.0

fig, ax = plt.subplots(figsize=(17, fig_h), facecolor=C["bg"])
ax.set_facecolor(C["bg"])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

# Column x positions and widths
col_x = [0.01, 0.115, 0.295, 0.475, 0.685, 0.87]   # left edge of each col
col_w = [c2 - c1 for c1, c2 in zip(col_x, col_x[1:] + [0.99])]

# ── Title ─────────────────────────────────────────────────────────────────────
ax.text(0.5, 0.975,
        "Competitive Landscape  —  AI Strategy Comparison",
        ha="center", va="top", fontsize=15, fontweight="bold", color=C["text"])
ax.text(0.5, 0.945,
        "Meridian Technologies  ·  Investor Day Prep  ·  February 2026  ·  CONFIDENTIAL",
        ha="center", va="top", fontsize=9, color=C["muted"])

# ── Helper: draw a cell ───────────────────────────────────────────────────────
def cell(x, y, w, h, bg, border=True, radius=0.004):
    rect = mpatches.FancyBboxPatch(
        (x + PAD*0.5, y + PAD*0.5), w - PAD, h - PAD,
        boxstyle=f"round,pad={radius}",
        facecolor=bg,
        edgecolor=C["border"] if border else "none",
        linewidth=0.6, zorder=2)
    ax.add_patch(rect)

def label(x, y, w, h, txt, color, size=8.8, weight="normal",
          ha="left", va="center", wrap=False):
    tx = x + PAD*1.5 if ha == "left" else x + w/2
    ty = y + h/2
    ax.text(tx, ty, txt, ha=ha, va=va,
            fontsize=size, color=color, fontweight=weight,
            linespacing=1.55, zorder=3)

# ── Header row ────────────────────────────────────────────────────────────────
headers   = ["Competitor", "AI Positioning", "Pricing Posture",
             "Latest Flagship\nAnnouncement", "Closer to\nMeridian Option"]
hdr_top   = 0.915
hdr_y     = hdr_top - HDR_H

for i, (hx, hw, htxt) in enumerate(zip(col_x, col_w, headers)):
    cell(hx, hdr_y, hw, HDR_H, bg=C["header_bg"], radius=0.005)
    label(hx, hdr_y, hw, HDR_H, htxt, C["bg"],
          size=9.5, weight="bold", ha="center")

# ── Data rows ─────────────────────────────────────────────────────────────────
for r, row in enumerate(rows):
    row_top = hdr_y - r * ROW_H
    row_y   = row_top - ROW_H
    bg      = C["row_alt"] if r % 2 else C["panel"]

    # Background strip
    cell(col_x[0], row_y, sum(col_w), ROW_H, bg=bg, border=False, radius=0.003)

    # Col 0 — Competitor name (coloured)
    cell(col_x[0], row_y, col_w[0], ROW_H, bg=row["color"] + "22", radius=0.005)
    label(col_x[0], row_y, col_w[0], ROW_H, row["name"],
          row["color"], size=10.5, weight="bold", ha="center")

    # Col 1 — AI positioning
    cell(col_x[1], row_y, col_w[1], ROW_H, bg=bg, radius=0.003)
    label(col_x[1], row_y, col_w[1], ROW_H, row["ai_pos"], C["text"], size=8.2)

    # Col 2 — Pricing posture
    cell(col_x[2], row_y, col_w[2], ROW_H, bg=bg, radius=0.003)
    label(col_x[2], row_y, col_w[2], ROW_H, row["pricing"], C["text"], size=8.2)

    # Col 3 — Flagship announcement
    cell(col_x[3], row_y, col_w[3], ROW_H, bg=bg, radius=0.003)
    label(col_x[3], row_y, col_w[3], ROW_H, row["flagship"], C["text"], size=8.2)

    # Col 4 — Option badge
    opt     = row["option"]
    opt_col = C["opt_b"] if opt == "B" else C["opt_a"]
    opt_lbl = f"Option {opt}"
    cell(col_x[4], row_y, col_w[4], ROW_H, bg=opt_col + "22", radius=0.005)

    # Big letter badge
    badge_x = col_x[4] + 0.012
    badge_y = row_y + ROW_H / 2
    ax.add_patch(mpatches.FancyBboxPatch(
        (badge_x, badge_y - 0.028), 0.038, 0.056,
        boxstyle="round,pad=0.004",
        facecolor=opt_col, edgecolor="none", zorder=3))
    ax.text(badge_x + 0.019, badge_y, opt,
            ha="center", va="center", fontsize=14,
            fontweight="bold", color=C["bg"], zorder=4)

    ax.text(badge_x + 0.048, badge_y + 0.012,
            opt_lbl, ha="left", va="center",
            fontsize=9, fontweight="bold", color=opt_col, zorder=3)
    ax.text(badge_x + 0.048, badge_y - 0.016,
            row["option_note"], ha="left", va="center",
            fontsize=7.5, color=C["muted"], zorder=3, linespacing=1.4)

# ── Divider lines between rows ────────────────────────────────────────────────
for r in range(n_rows + 1):
    ly = hdr_y - r * ROW_H
    ax.plot([col_x[0] + PAD, col_x[-1] + col_w[-1] - PAD],
            [ly, ly], color=C["border"], lw=0.5, zorder=1)

# ── Footer insight box ────────────────────────────────────────────────────────
footer_y = hdr_y - n_rows * ROW_H - 0.01
footer_h = 0.072

ax.add_patch(mpatches.FancyBboxPatch(
    (col_x[0] + PAD*0.5, footer_y - footer_h),
    sum(col_w) - PAD, footer_h,
    boxstyle="round,pad=0.004",
    facecolor=C["opt_b"] + "18",
    edgecolor=C["opt_b"], linewidth=1.0, zorder=2))

insight = (
    "Key finding:  Three of four competitors (Asana, Monday, Atlassian) are racing toward Option B — agentic platform, agents bundled or sold as premium. "
    "Smartsheet alone holds Option A,\n"
    "and its growth is decelerating to low single digits. "
    "If Meridian chooses Option B, the differentiator vs. the field is enterprise governance depth — which none of the three agentic competitors have built."
)
ax.text(col_x[0] + PAD*2, footer_y - footer_h / 2,
        insight, ha="left", va="center",
        fontsize=8.5, color=C["text"], linespacing=1.6, zorder=3)

# ── Source line ───────────────────────────────────────────────────────────────
ax.text(0.5, 0.005,
        "Sources: competitors_cached/ (Asana, Monday, Atlassian, Smartsheet)  ·  "
        "meridian_ai_strategy_options.md  ·  meridian_recent_customer_feedback.md",
        ha="center", va="bottom", fontsize=7, color=C["muted"])

plt.tight_layout(pad=0)
plt.savefig("competitive_landscape_table.png", dpi=150,
            bbox_inches="tight", facecolor=C["bg"])
print("Saved: competitive_landscape_table.png")
