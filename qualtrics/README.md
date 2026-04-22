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

## Quick Import (Recommended)

The generated QSF bundles every non-Conjoint block, the full Survey Flow, and all embedded-data defaults so that rebuilding the instrument on a fresh CLSBE Qualtrics account takes only a few clicks.

1. In Qualtrics → **Create new project** → **Survey** → **From a file** → upload `qsf-export/clsbe-cre-group3.qsf`.
2. All non-Conjoint blocks (01 Consent, 02 Pre-Task Covariates, 04a/04b Primers, 06 Manipulation Check, 07 Demographics, 08 Attention/Debrief/Lottery), plus the Survey Flow (embedded-data initializer, consent-fail branch, pressure randomizer) and the 16 embedded-data keys arrive pre-configured.
3. Blocks **05a Rating — High Pressure** and **05b Rating — Low Pressure** ship as placeholders. Add the Qualtrics **Conjoint** question to each block per `blocks/05-rating-task.md` and `conjoint-spec.json` (12 profiles, rating scale 1–7, attribute/level matrix from the JSON). Also replace the `[WARM-UP PLACEHOLDER]` in 04a and 04b with a 1-profile Conjoint warm-up question.
4. Paste the contents of `javascript/timer-high-pressure.js` into the **Question JS** of the 05a Conjoint question (and of the 04a warm-up Conjoint question).
5. Paste the contents of `javascript/response-time.js` into the **Question JS** of **both** 05a and 05b Conjoint questions (and, if you want warm-up timing, on the 04a/04b warm-ups too).
6. Run the full `qa-checklist.md` before activating the survey.

## How to import the survey into a fresh Qualtrics account (long form)
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
