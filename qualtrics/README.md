# Qualtrics Survey — CLSBE Bundle/Framing Study

This directory contains every artifact needed to rebuild the Qualtrics instrument from scratch.

## Files
- `survey-blueprint.md` — master spec (read first).
- `conjoint-spec.json` — attribute/level matrix consumed by Qualtrics Conjoint config and by the R analysis code.
- `blocks/` — one Markdown file per survey block with item-level specs.
- `javascript/` — Qualtrics JS snippets pasted into Question JS editors.
- `stimuli-plan.md` — meal-profile image composition spec.
- `qa-checklist.md` — manual pre-launch QA.
- `qsf-export/clsbe-cre-group3.qsf` — exported survey definition; source of truth for deployment.

## How to import the survey into a fresh Qualtrics account
1. Qualtrics home → **Create new project** → **From a file** → upload `qsf-export/clsbe-cre-group3.qsf`.
2. Open **Survey flow**; confirm the Randomizer branch (Block 3) and both primer/rating branches appear.
3. Run **Preview** twice; confirm one preview shows the 8-second timer and one does not.
4. Run **Test responses** (at least 5) to populate fake data; export `.csv` and check that `pressure`, per-profile `rt_ms_*`, and attribute columns are present.

## How to deploy
1. Activate survey → get distribution link.
2. Use anonymous link for WhatsApp / Telegram / mailing-list recruitment.
3. Monitor response count on the Qualtrics dashboard.

## How to export data
1. **Data & Analysis → Export & Import → Export Data → CSV**.
2. Choose **Use choice text** (not numeric codes) and **Include embedded data**.
3. Save the export to `data/raw/qualtrics_export_YYYY-MM-DD.csv`. `data/raw/` is gitignored — raw responses stay local.
