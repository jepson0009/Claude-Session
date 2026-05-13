# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

This is a strategic analysis and document-generation workspace for **Meridian Technologies** — a fictional B2B SaaS project-management company used as a case study. The repository contains:

- Source data files (CSVs, Markdown briefs, earnings call transcripts)
- Python scripts that generate charts (PNG) and a board presentation document (DOCX)
- Cached competitor research summaries
- Exercise data bundles (`exercise_1_data.zip`, `exercise_2_data.zip`)

There is no build system, test suite, or package manager. Scripts are run directly with Python.

## Running the Scripts

```bash
# Install dependencies (python-docx, matplotlib, pandas, numpy)
pip install python-docx matplotlib pandas numpy

# Generate the 12-panel quantitative deep-dive chart
python meridian_charts.py

# Generate the board document (requires meridian_quantitative_deepdive.png to exist first)
python build_board_doc.py        # outputs board_opening_remarks.docx

# Generate competitive landscape visuals
python competitive_slide.py      # outputs competitive_positioning_slide.png
python competitive_table.py      # outputs competitive_landscape_table.png

# Generate the positioning matrix
python positioning_matrix.py     # outputs positioning_matrix.png

# Generate salary distribution chart from toy HR data
python plot_salary.py            # outputs salary_distribution.png
```

`build_board_doc.py` embeds `meridian_quantitative_deepdive.png` directly into the DOCX, so run `meridian_charts.py` before `build_board_doc.py`.

## Data Files and Their Roles

| File | Contents |
|---|---|
| `meridian_financials_2022_2025.csv` | Quarterly revenue, ARR, margins, R&D/S&M spend (2022–2025) |
| `meridian_financials_summary.csv` | Annual summary version of the financials |
| `meridian_kpis_2024.csv` | NRR by segment, logo churn, magic number, CAC payback, Copilot seats |
| `toy_hr_data.csv` | Synthetic HR dataset used for salary analysis |

## Key Business Context

The strategic question driving this work: **Investor Day positioning decision** — should Meridian declare itself a "PM Platform with AI" (Option A) or an "Agentic Work Platform" (Option B)?

Key documents:
- `meridian_internal_brief.md` — CEO/CoS memo laying out the positioning dilemma and pointing to relevant source files
- `meridian_ai_strategy_options.md` — Detailed breakdown of Option A vs. Option B (pricing, hiring, M&A implications)
- `meridian_segments_overview.md` — ARR breakdown across SMB / Mid-Market / Enterprise
- `competitors.md` — Competitor URLs (Asana, Monday, Smartsheet, Atlassian) and instructions for fetching current AI positioning; fall back to `competitors_cached/` if live fetches fail

## Architecture of the Python Scripts

All scripts are self-contained (no shared modules). Each script:
1. Hard-codes or reads its own data (from CSVs or inline DataFrames)
2. Generates one or more output files (PNG or DOCX)
3. Prints a confirmation line on success

`build_board_doc.py` uses `python-docx` with low-level OOXML manipulation (via `OxmlElement` / `qn`) for paragraph shading and border rules — the standard `python-docx` API doesn't expose these, so direct XML manipulation is required.

`meridian_charts.py` and `competitive_slide.py` use Matplotlib with a dark-theme (`facecolor="#0F172A"`) and manual `GridSpec` layouts. All data is embedded as inline DataFrames rather than loaded from external files.
