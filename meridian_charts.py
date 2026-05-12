import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# ── Data ──────────────────────────────────────────────────────────────────────

fin = pd.DataFrame({
    "quarter": ["2022Q1","2022Q2","2022Q3","2022Q4",
                "2023Q1","2023Q2","2023Q3","2023Q4",
                "2024Q1","2024Q2","2024Q3","2024Q4",
                "2025Q1","2025Q2","2025Q3","2025Q4"],
    "revenue":  [60.4,64.1,67.3,68.6,73.0,76.2,79.4,82.0,
                 86.4,89.1,91.0,93.7,96.4,98.8,101.5,103.2],
    "arr":      [251.6,266.8,279.9,275.4,302.5,316.1,329.8,328.0,
                 357.5,367.6,374.1,374.8,398.9,408.5,419.6,412.8],
    "gross_margin": [77.8,77.9,78.0,78.2,78.4,78.5,78.6,78.7,
                     79.0,79.1,79.2,79.2,79.4,79.5,79.5,79.6],
    "op_margin":    [4.0,4.6,5.4,6.2,6.9,7.4,7.9,8.5,
                     9.4,9.8,10.1,10.5,11.1,11.6,12.0,12.4],
    "fcf_margin":   [7.5,9.1,11.2,13.8,12.5,13.6,14.2,15.4,
                     14.8,15.7,16.2,16.8,15.9,16.5,17.2,17.8],
    "sm_pct":   [40.2,39.5,38.9,38.2,37.6,37.1,36.5,36.0,
                 35.2,34.8,34.3,33.9,33.4,33.0,32.6,32.2],
    "rd_pct":   [21.5,21.8,21.9,22.1,22.4,22.6,23.0,23.2,
                 23.7,24.0,24.4,24.6,24.9,25.1,25.3,25.4],
    "cash":     [310.2,318.8,330.4,344.7,355.2,366.8,378.5,392.1,
                 401.4,412.6,420.9,431.5,438.2,447.0,455.8,463.4],
})

kpi = pd.DataFrame({
    "quarter": ["2024Q1","2024Q2","2024Q3","2024Q4",
                "2025Q1","2025Q2","2025Q3","2025Q4"],
    "nrr_overall":    [114,113,112,111,110,110,109,109],
    "nrr_smb":        [98, 96, 93, 91, 89, 88, 86, 84],
    "nrr_midmarket":  [108,107,106,105,104,103,103,102],
    "nrr_enterprise": [127,127,126,126,125,125,125,125],
    "grr_overall":    [89, 88, 88, 87, 87, 86, 86, 86],
    "logo_churn_smb": [18.4,19.1,19.8,20.2,20.8,21.1,21.6,22.1],
    "logo_churn_mid": [9.1, 9.4, 9.6, 9.8, 9.9,10.0,10.1,10.2],
    "logo_churn_ent": [3.2, 3.0, 2.9, 2.8, 2.7, 2.7, 2.6, 2.6],
    "magic_number":   [1.20,1.16,1.10,1.05,1.02,0.98,0.95,0.92],
    "cac_payback":    [18.2,18.9,19.5,20.4,21.1,21.6,22.0,22.4],
    "sales_prod":     [1320,1290,1255,1210,1180,1150,1130,1110],
    "copilot_seats":  [0,   0,   0,   0,   0,  140, 420, 710],
})

# ARR by segment (Q4 of each year, estimated from disclosures)
seg_arr = pd.DataFrame({
    "year":       ["2022","2023","2024","2025"],
    "Enterprise": [74,  101, 138, 167],
    "Mid-market": [96,  131, 168, 194],
    "SMB":        [106,  97,  69,  52],
})

# YoY revenue growth by year
ann = pd.DataFrame({
    "year":   ["2022","2023","2024","2025"],
    "rev":    [260.4, 310.6, 360.2, 399.9],
    "growth": [None, 19.3, 16.0, 11.0],   # approx
})

# ── Figure setup ──────────────────────────────────────────────────────────────
BLUE   = "#2563EB"
RED    = "#DC2626"
AMBER  = "#D97706"
GREEN  = "#16A34A"
GRAY   = "#6B7280"
LIGHT  = "#F3F4F6"

fig = plt.figure(figsize=(18, 22))
fig.patch.set_facecolor("white")

quarters_fin = fin["quarter"]
quarters_kpi = kpi["quarter"]

def ax_style(ax, title):
    ax.set_facecolor(LIGHT)
    ax.set_title(title, fontsize=11, fontweight="bold", pad=8)
    ax.tick_params(labelsize=8)
    ax.spines[["top","right","left","bottom"]].set_visible(False)
    ax.yaxis.grid(True, color="white", linewidth=1.2)
    ax.set_axisbelow(True)

# ── 1. Revenue growth deceleration ───────────────────────────────────────────
ax1 = fig.add_subplot(4, 3, 1)
bars = ax1.bar(ann["year"], [19.3, 19.3, 16.0, 11.0],
               color=[GRAY, BLUE, BLUE, RED], width=0.5, zorder=3)
for bar, val in zip(bars, [19.3, 19.3, 16.0, 11.0]):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
             f"{val}%", ha="center", va="bottom", fontsize=9, fontweight="bold")
ax1.set_ylim(0, 26)
ax1.set_ylabel("YoY Growth (%)", fontsize=8)
ax_style(ax1, "1. Revenue Growth Deceleration")
ax1.set_xlabel("Year", fontsize=8)
# annotation
ax1.annotate("28% in 2022", xy=(0, 19.3), xytext=(0.3, 23),
             fontsize=7.5, color=GRAY,
             arrowprops=dict(arrowstyle="->", color=GRAY, lw=0.8))

# ── 2. ARR trajectory ─────────────────────────────────────────────────────────
ax2 = fig.add_subplot(4, 3, 2)
ax2.plot(quarters_fin, fin["arr"], color=BLUE, lw=2.5, marker="o", ms=4, zorder=3)
# shade Q4 2025 dip
ax2.annotate("ARR dips Q4\n($419→$413M)", xy=(15, 412.8), xytext=(12, 390),
             fontsize=7.5, color=RED,
             arrowprops=dict(arrowstyle="->", color=RED, lw=0.8))
ax2.set_ylabel("ARR ($M)", fontsize=8)
ax2.set_xticks(range(0, 16, 2))
ax2.set_xticklabels([quarters_fin.iloc[i] for i in range(0, 16, 2)], rotation=30, ha="right")
ax_style(ax2, "2. ARR Trajectory (2022–2025)")

# ── 3. ARR mix shift ──────────────────────────────────────────────────────────
ax3 = fig.add_subplot(4, 3, 3)
x = np.arange(len(seg_arr["year"]))
w = 0.22
b1 = ax3.bar(x - w, seg_arr["Enterprise"], w, label="Enterprise", color=GREEN, zorder=3)
b2 = ax3.bar(x,     seg_arr["Mid-market"], w, label="Mid-market", color=BLUE,  zorder=3)
b3 = ax3.bar(x + w, seg_arr["SMB"],        w, label="SMB",        color=RED,   zorder=3)
ax3.set_xticks(x); ax3.set_xticklabels(seg_arr["year"])
ax3.set_ylabel("ARR ($M)", fontsize=8)
ax3.legend(fontsize=7.5, frameon=False)
ax_style(ax3, "3. ARR Mix Shift by Segment")

# ── 4. NRR by segment ─────────────────────────────────────────────────────────
ax4 = fig.add_subplot(4, 3, 4)
ax4.plot(quarters_kpi, kpi["nrr_enterprise"], color=GREEN, lw=2.5, marker="o", ms=4, label="Enterprise", zorder=3)
ax4.plot(quarters_kpi, kpi["nrr_midmarket"],  color=BLUE,  lw=2.5, marker="s", ms=4, label="Mid-market", zorder=3)
ax4.plot(quarters_kpi, kpi["nrr_smb"],        color=RED,   lw=2.5, marker="^", ms=4, label="SMB",        zorder=3)
ax4.axhline(100, color="black", lw=1, linestyle="--", alpha=0.5, label="100% (breakeven)")
ax4.set_ylabel("NRR (%)", fontsize=8)
ax4.set_ylim(78, 135)
ax4.legend(fontsize=7.5, frameon=False)
ax4.set_xticks(range(len(quarters_kpi))); ax4.set_xticklabels(quarters_kpi, rotation=30, ha="right")
ax_style(ax4, "4. Net Revenue Retention by Segment")
# mid-market arrow
ax4.annotate("Mid-market: 108→102%\napproaching breakeven",
             xy=(7, 102), xytext=(4, 94),
             fontsize=7, color=BLUE,
             arrowprops=dict(arrowstyle="->", color=BLUE, lw=0.8))

# ── 5. Gross logo churn by segment ───────────────────────────────────────────
ax5 = fig.add_subplot(4, 3, 5)
ax5.plot(quarters_kpi, kpi["logo_churn_smb"], color=RED,   lw=2.5, marker="^", ms=4, label="SMB",        zorder=3)
ax5.plot(quarters_kpi, kpi["logo_churn_mid"], color=BLUE,  lw=2.5, marker="s", ms=4, label="Mid-market", zorder=3)
ax5.plot(quarters_kpi, kpi["logo_churn_ent"], color=GREEN, lw=2.5, marker="o", ms=4, label="Enterprise", zorder=3)
ax5.set_ylabel("Gross Logo Churn (% annual)", fontsize=8)
ax5.legend(fontsize=7.5, frameon=False)
ax5.set_xticks(range(len(quarters_kpi))); ax5.set_xticklabels(quarters_kpi, rotation=30, ha="right")
ax_style(ax5, "5. Gross Logo Churn by Segment")

# ── 6. Magic number & CAC payback ────────────────────────────────────────────
ax6 = fig.add_subplot(4, 3, 6)
ax6_r = ax6.twinx()
ax6.plot(quarters_kpi, kpi["magic_number"], color=BLUE,  lw=2.5, marker="o", ms=4, label="Magic Number (L)", zorder=3)
ax6_r.plot(quarters_kpi, kpi["cac_payback"], color=AMBER, lw=2.5, marker="s", ms=4, label="CAC Payback months (R)", zorder=3)
ax6.axhline(1.0, color=BLUE, lw=0.8, linestyle="--", alpha=0.6)
ax6.set_ylabel("Magic Number", fontsize=8, color=BLUE)
ax6_r.set_ylabel("CAC Payback (months)", fontsize=8, color=AMBER)
ax6.set_ylim(0.7, 1.4)
ax6_r.set_ylim(15, 26)
lines1, labels1 = ax6.get_legend_handles_labels()
lines2, labels2 = ax6_r.get_legend_handles_labels()
ax6.legend(lines1+lines2, labels1+labels2, fontsize=7, frameon=False, loc="lower left")
ax6.set_xticks(range(len(quarters_kpi))); ax6.set_xticklabels(quarters_kpi, rotation=30, ha="right")
ax6.set_facecolor(LIGHT)
ax6.set_title("6. Sales Efficiency Deteriorating", fontsize=11, fontweight="bold", pad=8)
ax6.spines[["top","right","left","bottom"]].set_visible(False)
ax6.yaxis.grid(True, color="white", linewidth=1.2)
ax6.set_axisbelow(True)
ax6.tick_params(labelsize=8)
ax6_r.tick_params(labelsize=8)
ax6_r.spines[["top","left","bottom"]].set_visible(False)

# ── 7. Operating margin expansion ─────────────────────────────────────────────
ax7 = fig.add_subplot(4, 3, 7)
ax7.fill_between(range(16), fin["fcf_margin"], alpha=0.25, color=GREEN)
ax7.plot(range(16), fin["op_margin"],  color=BLUE,  lw=2.5, marker="o", ms=3, label="Operating margin")
ax7.plot(range(16), fin["fcf_margin"], color=GREEN, lw=2.5, marker="s", ms=3, label="FCF margin")
ax7.set_xticks(range(0, 16, 2))
ax7.set_xticklabels([quarters_fin.iloc[i] for i in range(0, 16, 2)], rotation=30, ha="right")
ax7.set_ylabel("Margin (%)", fontsize=8)
ax7.legend(fontsize=7.5, frameon=False)
ax_style(ax7, "7. Margin Expansion (Good News)")

# ── 8. R&D vs S&M spend ───────────────────────────────────────────────────────
ax8 = fig.add_subplot(4, 3, 8)
ax8.plot(range(16), fin["rd_pct"], color=BLUE,  lw=2.5, marker="o", ms=3, label="R&D % revenue", zorder=3)
ax8.plot(range(16), fin["sm_pct"], color=AMBER, lw=2.5, marker="s", ms=3, label="S&M % revenue", zorder=3)
ax8.set_xticks(range(0, 16, 2))
ax8.set_xticklabels([quarters_fin.iloc[i] for i in range(0, 16, 2)], rotation=30, ha="right")
ax8.set_ylabel("% of Revenue", fontsize=8)
ax8.legend(fontsize=7.5, frameon=False)
ax_style(ax8, "8. R&D Rising, S&M Falling")
ax8.annotate("R&D highest\nsince IPO", xy=(15, 25.4), xytext=(11, 26.5),
             fontsize=7.5, color=BLUE,
             arrowprops=dict(arrowstyle="->", color=BLUE, lw=0.8))

# ── 9. AI Copilot seat ramp ───────────────────────────────────────────────────
ax9 = fig.add_subplot(4, 3, 9)
copilot_q = ["2025Q1","2025Q2","2025Q3","2025Q4"]
copilot_s  = [0, 140, 420, 710]
colors9 = [GRAY, BLUE, BLUE, GREEN]
bars9 = ax9.bar(copilot_q, copilot_s, color=colors9, width=0.5, zorder=3)
for bar, val in zip(bars9, copilot_s):
    ax9.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + 8, str(val),
             ha="center", va="bottom", fontsize=9, fontweight="bold")
ax9.set_ylabel("Paying Seats", fontsize=8)
ax9.set_ylim(0, 900)
ax_style(ax9, "9. AI Copilot Paying Seats Ramp")
ax9.annotate("GA: Sept 2025", xy=(2, 420), xytext=(1.0, 650),
             fontsize=7.5, color=GRAY,
             arrowprops=dict(arrowstyle="->", color=GRAY, lw=0.8))

# ── 10. Cash position ─────────────────────────────────────────────────────────
ax10 = fig.add_subplot(4, 3, 10)
ax10.fill_between(range(16), fin["cash"], alpha=0.2, color=GREEN)
ax10.plot(range(16), fin["cash"], color=GREEN, lw=2.5, marker="o", ms=3, zorder=3)
ax10.set_xticks(range(0, 16, 2))
ax10.set_xticklabels([quarters_fin.iloc[i] for i in range(0, 16, 2)], rotation=30, ha="right")
ax10.set_ylabel("Cash ($M)", fontsize=8)
ax10.annotate("Helio close\n($10M cash)", xy=(15, 463.4), xytext=(11, 445),
             fontsize=7.5, color=GRAY,
             arrowprops=dict(arrowstyle="->", color=GRAY, lw=0.8))
ax_style(ax10, "10. Cash Position ($463M, No Debt)")

# ── 11. Sales rep productivity ────────────────────────────────────────────────
ax11 = fig.add_subplot(4, 3, 11)
ax11.plot(quarters_kpi, kpi["sales_prod"], color=RED, lw=2.5, marker="o", ms=4, zorder=3)
ax11.set_ylabel("New ARR per Rep ($K)", fontsize=8)
ax11.set_ylim(1000, 1400)
ax11.set_xticks(range(len(quarters_kpi))); ax11.set_xticklabels(quarters_kpi, rotation=30, ha="right")
ax_style(ax11, "11. Sales Productivity Declining")
ax11.annotate(f"−16% in 8 quarters\n($1,320K → $1,110K)",
              xy=(7, 1110), xytext=(3, 1130),
              fontsize=7.5, color=RED,
              arrowprops=dict(arrowstyle="->", color=RED, lw=0.8))

# ── 12. The mid-market risk summary ──────────────────────────────────────────
ax12 = fig.add_subplot(4, 3, 12)
ax12.set_facecolor(LIGHT)
ax12.set_xlim(0, 1); ax12.set_ylim(0, 1)
ax12.axis("off")
ax12.set_title("12. Mid-Market: The Risk Summary", fontsize=11, fontweight="bold", pad=8)
rows = [
    ("Metric",              "2022",   "2025Q4",  "Direction"),
    ("NRR",                 "115%",   "102%",    "↓ 13 pts"),
    ("Gross Logo Churn",    "~9%",    "10.2%",   "↓ Worsening"),
    ("ARR Share",           "35%",    "47%",     "↑ Larger exposure"),
    ("ARR ($M)",            "$96M",   "$194M",   "↑ More at risk"),
    ("Breakeven NRR",       "100%",   "100%",    "→ 2 pts away"),
]
col_x = [0.02, 0.28, 0.50, 0.72]
for r, row in enumerate(rows):
    y = 0.88 - r * 0.14
    for c, (val, x) in enumerate(zip(row, col_x)):
        weight = "bold" if r == 0 else "normal"
        color  = RED if (r > 0 and c == 3) else ("black" if r == 0 else "#1F2937")
        ax12.text(x, y, val, fontsize=8, fontweight=weight, color=color,
                  va="top", transform=ax12.transAxes)
    if r == 0:
        ax12.plot([0.01, 0.99], [y - 0.04, y - 0.04],
                  color=GRAY, lw=0.8, transform=ax12.transAxes, clip_on=False)

# ── Title & layout ────────────────────────────────────────────────────────────
fig.suptitle("Meridian Technologies — Board Strategic Review: Quantitative Deep-Dive",
             fontsize=14, fontweight="bold", y=0.995)

plt.tight_layout(rect=[0, 0, 1, 0.995])
plt.savefig("meridian_quantitative_deepdive.png", dpi=150, bbox_inches="tight")
print("Saved: meridian_quantitative_deepdive.png")
