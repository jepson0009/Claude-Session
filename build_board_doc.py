from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

doc = Document()

# ── Page margins ──────────────────────────────────────────────────────────────
for section in doc.sections:
    section.top_margin    = Inches(0.85)
    section.bottom_margin = Inches(0.85)
    section.left_margin   = Inches(1.0)
    section.right_margin  = Inches(1.0)

# ── Helpers ───────────────────────────────────────────────────────────────────
DARK   = RGBColor(0x1F, 0x29, 0x37)   # near-black
BLUE   = RGBColor(0x25, 0x63, 0xEB)   # accent blue
RED    = RGBColor(0xDC, 0x26, 0x26)   # alert red
GRAY   = RGBColor(0x6B, 0x72, 0x80)   # muted gray
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)

def add_para(doc, text="", style="Normal", space_before=0, space_after=6,
             bold=False, italic=False, font_size=11,
             color=DARK, align=WD_ALIGN_PARAGRAPH.LEFT, keep_with_next=False):
    p = doc.add_paragraph(style=style)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after  = Pt(space_after)
    p.paragraph_format.alignment    = align
    if keep_with_next:
        p.paragraph_format.keep_with_next = True
    if text:
        run = p.add_run(text)
        run.bold      = bold
        run.italic    = italic
        run.font.size = Pt(font_size)
        run.font.color.rgb = color
    return p

def add_run(para, text, bold=False, italic=False, font_size=11, color=DARK):
    run = para.add_run(text)
    run.bold      = bold
    run.italic    = italic
    run.font.size = Pt(font_size)
    run.font.color.rgb = color
    return run

def add_shaded_para(doc, text, bg_hex="2563EB", font_color=WHITE,
                    font_size=11, bold=False, space_before=6, space_after=6,
                    left_indent=0):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after  = Pt(space_after)
    if left_indent:
        p.paragraph_format.left_indent = Inches(left_indent)
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), bg_hex)
    pPr.append(shd)
    run = p.add_run(text)
    run.bold = bold
    run.font.size = Pt(font_size)
    run.font.color.rgb = font_color
    return p

def add_rule(doc, color_hex="2563EB", thickness=12):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(0)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), str(thickness))
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), color_hex)
    pBdr.append(bottom)
    pPr.append(pBdr)
    return p

# ═══════════════════════════════════════════════════════════════════════════════
# HEADER BLOCK
# ═══════════════════════════════════════════════════════════════════════════════

# Meta line
meta = doc.add_paragraph()
meta.paragraph_format.space_before = Pt(0)
meta.paragraph_format.space_after  = Pt(2)
add_run(meta, "MERIDIAN TECHNOLOGIES  ·  BOARD STRATEGIC REVIEW  ·  ", bold=True, font_size=8, color=BLUE)
add_run(meta, "CONFIDENTIAL", bold=True, font_size=8, color=RED)

# Headline
hl = doc.add_paragraph()
hl.paragraph_format.space_before = Pt(4)
hl.paragraph_format.space_after  = Pt(4)
add_run(hl,
    "Meridian has one healthy engine, one stalling engine, and one burning — "
    "and twelve months to decide which bets to make before the AI window closes.",
    bold=True, font_size=15, color=DARK)

add_rule(doc, color_hex="2563EB", thickness=18)

# Speaker / occasion line
occ = doc.add_paragraph()
occ.paragraph_format.space_before = Pt(6)
occ.paragraph_format.space_after  = Pt(14)
add_run(occ, "Catherine Park, CEO  ·  Annual Board Strategic Review  ·  Opening Remarks (~5 min)",
        italic=True, font_size=9, color=GRAY)

# ═══════════════════════════════════════════════════════════════════════════════
# OPENING
# ═══════════════════════════════════════════════════════════════════════════════

add_para(doc, "Opening", bold=True, font_size=10, color=BLUE,
         space_before=0, space_after=3, keep_with_next=True)

opening = doc.add_paragraph()
opening.paragraph_format.space_before = Pt(0)
opening.paragraph_format.space_after  = Pt(10)
add_run(opening,
    "Thank you. My five minutes, used directly. "
    "This is my first annual review as your CEO. "
    "I have spent the year making early bets — segment reorg, AI acquisition, harder line on SMB. "
    "I believe those were right. But I'm not here to declare victory. "
    "I'm here to tell you what worries me and what I need from this board.",
    font_size=11, color=DARK)

# ═══════════════════════════════════════════════════════════════════════════════
# ISSUE 1
# ═══════════════════════════════════════════════════════════════════════════════

add_shaded_para(doc, "  ISSUE 1 OF 3   The AI race: early signs of life, but we are not yet safe.",
                bg_hex="2563EB", font_color=WHITE, bold=True, font_size=10.5,
                space_before=10, space_after=0)

i1 = doc.add_paragraph()
i1.paragraph_format.space_before = Pt(6)
i1.paragraph_format.space_after  = Pt(10)
i1.paragraph_format.left_indent  = Inches(0.15)
add_run(i1,
    "Copilot hit GA in September: 710 paying seats, 44% attach on Q4 enterprise renewals, "
    "$3.5M ARR. Early proof points — not yet a growth driver. "
    "Meanwhile Asana bundled AI into its standard tier; Monday surpassed us by ARR; "
    "Atlassian's agentic Jira enters our enterprise deals directly for the first time. "
    "Our magic number fell from 1.20 to 0.92 over eight quarters ",
    font_size=11, color=DARK)
add_run(i1, "(meridian_kpis_2024.csv)", italic=True, font_size=10, color=GRAY)
add_run(i1,
    "; CAC payback stretched from 18 to 22 months. "
    "R&D is at 25.4% of revenue — highest since IPO — and it is not yet showing up in growth. "
    "The board needs to weigh in on one pricing question: hold $40/seat add-on or bundle "
    "Copilot into mid-market to defend NRR? That is a strategic decision, not a product one.",
    font_size=11, color=DARK)

# ═══════════════════════════════════════════════════════════════════════════════
# ISSUE 2
# ═══════════════════════════════════════════════════════════════════════════════

add_shaded_para(doc, "  ISSUE 2 OF 3   Mid-market erosion: the hidden time bomb.",
                bg_hex="DC2626", font_color=WHITE, bold=True, font_size=10.5,
                space_before=10, space_after=0)

i2 = doc.add_paragraph()
i2.paragraph_format.space_before = Pt(6)
i2.paragraph_format.space_after  = Pt(10)
i2.paragraph_format.left_indent  = Inches(0.15)
add_run(i2, "Mid-market is 47% of our ARR — $194M — our single largest segment. ",
        bold=True, font_size=11, color=DARK)
add_run(i2,
    "NRR has compressed from 115% in 2022 to 102% today, declining every single quarter "
    "for three years (Chart 4). Gross logo churn has risen from 9.1% to 10.2%. "
    "At 102%, mid-market is barely generating net expansion — "
    "two quarters away from shrinking in absolute ARR. ",
    font_size=11, color=DARK)
add_run(i2, "(meridian_segments_overview.md; meridian_kpis_2024.csv)",
        italic=True, font_size=10, color=GRAY)
add_run(i2,
    "\n\nThe trigger is live: Asana bundles AI at no extra charge and our customers know it. "
    "The resource management module — top-three customer ask — has been deferred twice, now to Q2 2026. "
    "We have no specific intervention yet that breaks the compression curve. "
    "This is the issue that can be invisible in the headlines until it isn't.",
    font_size=11, color=DARK)

# ═══════════════════════════════════════════════════════════════════════════════
# ISSUE 3
# ═══════════════════════════════════════════════════════════════════════════════

add_shaded_para(doc, "  ISSUE 3 OF 3   Organizational capacity: the binding constraint on all of it.",
                bg_hex="D97706", font_color=WHITE, bold=True, font_size=10.5,
                space_before=10, space_after=0)

i3 = doc.add_paragraph()
i3.paragraph_format.space_before = Pt(6)
i3.paragraph_format.space_after  = Pt(10)
i3.paragraph_format.left_indent  = Inches(0.15)
add_run(i3,
    "We are running five parallel tracks in 2026: Helio integration, new AI product suite, "
    "pricing model transition, three segment P&Ls going live, and Investor Day in six weeks. "
    "The survey is clear: 31% of engineers cited 'roadmap thrash' — three AI pivots in 18 months. "
    "19% company-wide said they no longer know what Meridian stands for. "
    "Six of twelve 2025 commitments slipped; two were deferred. ",
    font_size=11, color=DARK)
add_run(i3, "(meridian_employee_survey_2025.md; meridian_product_roadmap_2025.md)",
        italic=True, font_size=10, color=GRAY)
add_run(i3,
    "\n\nFor the Compensation Committee: 27% of senior engineers flagged pay. "
    "People team estimates 15–25 at imminent attrition risk. "
    "Helio's cash cliff arrives in 2026 — if that team unwinds early, "
    "the agent-builder roadmap loses its architects.",
    font_size=11, color=DARK)

# ═══════════════════════════════════════════════════════════════════════════════
# MY ONE ASK
# ═══════════════════════════════════════════════════════════════════════════════

add_rule(doc, color_hex="1F2937", thickness=8)

ask_heading = doc.add_paragraph()
ask_heading.paragraph_format.space_before = Pt(10)
ask_heading.paragraph_format.space_after  = Pt(4)
add_run(ask_heading, "My One Ask of This Board", bold=True, font_size=12, color=DARK)

ask_body = doc.add_paragraph()
ask_body.paragraph_format.space_before = Pt(0)
ask_body.paragraph_format.space_after  = Pt(10)
add_run(ask_body,
    "Plan approval comes at Investor Day, March 11. Today I have one ask: ",
    font_size=11, color=DARK)
add_run(ask_body,
    "a board position on mid-market Copilot pricing before we leave this room.",
    bold=True, font_size=11, color=DARK)
add_run(ask_body,
    " Hold $40/seat add-on and accept potential NRR compression — "
    "or authorize a Q1 bundling trial for mid-market renewals to defend the segment? "
    "That decision touches 2026 revenue guidance, operating margin, and competitive positioning. "
    "It cannot wait until March. Everything else I can manage. This one I need the board to own with me.",
    font_size=11, color=DARK)

# ═══════════════════════════════════════════════════════════════════════════════
# CHART
# ═══════════════════════════════════════════════════════════════════════════════

add_rule(doc, color_hex="2563EB", thickness=8)

chart_heading = doc.add_paragraph()
chart_heading.paragraph_format.space_before = Pt(10)
chart_heading.paragraph_format.space_after  = Pt(4)
add_run(chart_heading, "Supporting Data — Quantitative Deep-Dive",
        bold=True, font_size=11, color=DARK)

cap = doc.add_paragraph()
cap.paragraph_format.space_before = Pt(0)
cap.paragraph_format.space_after  = Pt(8)
add_run(cap,
    "The 12-panel chart below covers all key trends cited above. "
    "Panels 4 and 12 are most directly relevant to Issue 2. "
    "Panel 6 (magic number / CAC payback) supports Issue 1. "
    "Full data sources: meridian_financials_2022_2025.csv and meridian_kpis_2024.csv.",
    italic=True, font_size=9.5, color=GRAY)

doc.add_picture("meridian_quantitative_deepdive.png", width=Inches(6.4))
last_para = doc.paragraphs[-1]
last_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

img_cap = doc.add_paragraph()
img_cap.paragraph_format.space_before = Pt(4)
img_cap.paragraph_format.space_after  = Pt(10)
img_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
add_run(img_cap,
    "Figure 1: Meridian Technologies — Board Strategic Review Quantitative Deep-Dive  "
    "|  Source: meridian_financials_2022_2025.csv, meridian_kpis_2024.csv",
    italic=True, font_size=8, color=GRAY)

# ═══════════════════════════════════════════════════════════════════════════════
# CLOSING
# ═══════════════════════════════════════════════════════════════════════════════

closing = doc.add_paragraph()
closing.paragraph_format.space_before = Pt(6)
closing.paragraph_format.space_after  = Pt(0)
add_run(closing,
    "I am proud of what this team has done in a difficult year. "
    "I am clear-eyed about what remains undone. "
    "Let's get to work.",
    italic=True, font_size=11, color=DARK)

# ── Footer note ───────────────────────────────────────────────────────────────
fn = doc.add_paragraph()
fn.paragraph_format.space_before = Pt(18)
fn.paragraph_format.space_after  = Pt(0)
add_run(fn,
    "Confidential — prepared for the Meridian Technologies Board of Directors.  "
    "Not for distribution.",
    font_size=8, color=GRAY, italic=True)

doc.save("board_opening_remarks.docx")
print("Saved: board_opening_remarks.docx")
