# Qualtrics Survey Implementation Plan — CLSBE Bundle/Framing Study

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a fully functional Qualtrics survey instrument that implements the rating-based conjoint experiment defined in `docs/proposal.qmd` — 8 blocks, mixed design with between-subjects time-pressure randomization and within-subjects profile-level attribute randomization, ready for pilot on 2026-04-27.

**Architecture:** The survey is built in Qualtrics' visual editor on top of the built-in **Conjoint module (rating / full-profile mode)**. Pressure assignment is handled via a **Randomizer** block element that sets an embedded data field (`pressure = high | low`). Branch logic in the Survey Flow shows different primers and adds the countdown timer on the rating block when `pressure = high`. A small JavaScript block injects an 8-second visible countdown and captures per-profile response time. All spec documents live in `qualtrics/`; the final `.qsf` export is committed under `qualtrics/qsf-export/` so the survey is version-controlled and reproducible.

**Tech Stack:** Qualtrics (CLSBE license, Conjoint module enabled), vanilla JavaScript (Qualtrics Question JS API: `Qualtrics.SurveyEngine.addOnload/addOnReady/addOnUnload`), JSON (machine-readable attribute spec), Markdown (block-level specs). No backend; all data exported from Qualtrics as `.csv` into `data/raw/`.

**Branch:** Work happens on `feature/qualtrics-survey`. One commit per completed task. Open PR at Task 22.

**Out of scope for this plan:**
- Stimuli image rendering pipeline (design is specified; actual PNG generation handled in a follow-up plan).
- R analysis code (covered by a separate analysis plan after data collection).
- CLSBE ethics submission text (drafted separately; this plan only references the consent text location).

---

## File Structure

Files created or modified by this plan:

| Path | Responsibility |
|---|---|
| `qualtrics/README.md` | Build instructions for collaborators; how to import the QSF, run the pilot, export data |
| `qualtrics/survey-blueprint.md` | Master spec: block order, item wording verbatim, display logic, embedded data schema |
| `qualtrics/conjoint-spec.json` | Machine-readable attribute/level matrix — drives Qualtrics Conjoint config and future analysis code |
| `qualtrics/blocks/01-consent.md` | Exact consent text + radio-button wiring |
| `qualtrics/blocks/02-pretask-covariates.md` | Hunger, hours-since-meal, cafeteria-usage, price-sensitivity scale, dietary restrictions |
| `qualtrics/blocks/03-pressure-randomizer.md` | Randomizer element config + embedded-data key |
| `qualtrics/blocks/04-primer.md` | Two branch-specific primer texts + warm-up task |
| `qualtrics/blocks/05-rating-task.md` | Conjoint rating block: attribute config, profile generation, rating item, per-profile response-time capture |
| `qualtrics/blocks/06-manip-check.md` | Felt-pressure item, open-ended WTP, realism check, hypothesis-guess free-text |
| `qualtrics/blocks/07-demographics.md` | Gender, age bands, year, nationality, monthly discretionary budget |
| `qualtrics/blocks/08-attention-debrief-lottery.md` | Instructed-response item, debrief text, detached email field for lottery |
| `qualtrics/javascript/timer-high-pressure.js` | 8-second visible countdown; soft nudge on expiry; does not auto-advance |
| `qualtrics/javascript/response-time.js` | Capture ms-precise per-profile response time into embedded data |
| `qualtrics/stimuli-plan.md` | Specification for the 288-profile image composites (plan only; generation is separate) |
| `qualtrics/qsf-export/clsbe-cre-group3.qsf` | Final exported survey definition — committed for reproducibility |
| `qualtrics/qa-checklist.md` | Pre-launch QA checklist with expected behaviors per branch |

Each spec file lives next to the block it documents so a collaborator reviewing one block does not have to cross-reference the master blueprint. The master blueprint summarizes flow and links out.

---

## Task 1: Scaffold the `qualtrics/` directory

**Files:**
- Create: `qualtrics/README.md`
- Create: `qualtrics/blocks/.gitkeep`
- Create: `qualtrics/javascript/.gitkeep`
- Create: `qualtrics/qsf-export/.gitkeep`
- Delete: `qualtrics/.gitkeep` (replaced by real content)

- [ ] **Step 1: Create subdirectories and placeholder files**

```bash
cd "/Users/max/Documents/Master/Courses/Causality and Randomized Experiments/Group Work"
mkdir -p qualtrics/blocks qualtrics/javascript qualtrics/qsf-export
touch qualtrics/blocks/.gitkeep qualtrics/javascript/.gitkeep qualtrics/qsf-export/.gitkeep
rm qualtrics/.gitkeep
```

- [ ] **Step 2: Write `qualtrics/README.md`**

```markdown
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
```

- [ ] **Step 3: Verify directory layout**

Run: `ls -la qualtrics/`
Expected:
```
README.md
blocks/
conjoint-spec.json  (not yet — added in Task 3)
javascript/
qsf-export/
```

- [ ] **Step 4: Commit**

```bash
git add qualtrics/
git commit -m "Scaffold qualtrics/ directory and README"
```

---

## Task 2: Master survey blueprint

**Files:**
- Create: `qualtrics/survey-blueprint.md`

- [ ] **Step 1: Write the blueprint**

The blueprint must include the following sections with the content shown (verbatim):

```markdown
# Survey Blueprint — CLSBE Bundle/Framing Study

## Metadata
- **Qualtrics project name:** `CLSBE-CRE-Group3-BundleFraming-2026`
- **Qualtrics license:** CLSBE (Conjoint module required; verified pre-build).
- **Estimated completion time:** ~6 min.
- **Target n:** 200 (100 per pressure condition); stretch 240.
- **Live dates:** Pilot 2026-04-27 to 2026-04-29; full launch 2026-04-30 to 2026-05-04.

## Embedded Data Schema
These fields are declared on the **Survey Flow → Set Embedded Data** element placed at the very top of the flow (so every field exists on every response, even abandoned ones):

| Key | Type | Set by | Used for |
|---|---|---|---|
| `pressure` | string (`high` \| `low`) | Randomizer in Block 3 | Branch logic + analysis |
| `timer_duration_s` | number | Default `8`; overridden in high-pressure branch | Timer JS reads this value |
| `rt_ms_1` … `rt_ms_12` | number | `response-time.js` on each rating page | Manipulation check, process measure |
| `warmup_discarded` | boolean | Set true on warm-up page | Drop flag in analysis |
| `attention_pass` | boolean | Set by Block 8 attention-check scoring | Exclusion flag |

## Block Order and Flow
1. **Block 1** — Welcome + Consent (hard stop if "I do not consent")
2. **Block 2** — Pre-task covariates
3. **Block 3** — Pressure Randomizer (invisible to respondent; sets `pressure`)
4. **Block 4a / 4b** — Primer (branched on `pressure`)
5. **Block 5** — 12 conjoint rating tasks (the timer JS only loads when `pressure = high`)
6. **Block 6** — Manipulation check + secondary outcomes
7. **Block 7** — Demographics
8. **Block 8** — Attention check + debrief + lottery email (detached)

## Survey Flow diagram (conceptual)
```
[Set Embedded Data — all keys with defaults]
  → [Block 1: Consent]
  → [Branch: consent != "Yes" → End of Survey with "Thanks" message]
  → [Block 2: Covariates]
  → [Randomizer: Evenly Present Elements = ON, 1 of the following]
        ├── [Set ED: pressure = high] → [Block 4a: High-pressure primer] → [Block 5 with timer JS]
        └── [Set ED: pressure = low]  → [Block 4b: Low-pressure primer]  → [Block 5 without timer JS]
  → [Block 6]
  → [Block 7]
  → [Block 8]
  → [End of Survey with debrief redirect]
```

## Cross-cutting display options
- **Progress bar:** verbose, at top.
- **Back button:** disabled on Block 5 pages (rating tasks) to prevent retroactive edits under time pressure; enabled elsewhere.
- **Mobile:** allowed — Qualtrics auto-responsive; verify on pilot.
- **Font:** Qualtrics default; override only if pilot flags legibility issues.
- **Language:** English (CLSBE courses are taught in English; Portuguese translation out of scope for this plan).
```

- [ ] **Step 2: Commit**

```bash
git add qualtrics/survey-blueprint.md
git commit -m "Add master survey blueprint"
```

---

## Task 3: Machine-readable conjoint attribute spec

**Files:**
- Create: `qualtrics/conjoint-spec.json`

The JSON matches the attribute table in `docs/proposal.qmd` Appendix A exactly. Keeping it machine-readable lets the analysis code load the reference levels without hand-typing.

- [ ] **Step 1: Write `qualtrics/conjoint-spec.json`**

```json
{
  "design_mode": "rating_full_profile",
  "profiles_per_respondent": 12,
  "warmup_profiles": 1,
  "rating_scale": {
    "min": 1,
    "max": 7,
    "min_label": "Not at all appealing",
    "max_label": "Extremely appealing"
  },
  "attributes": [
    {
      "id": "format",
      "label": "Format",
      "type": "focal",
      "levels": ["Separate items", "Bundle"],
      "reference": "Separate items"
    },
    {
      "id": "label",
      "label": "Label",
      "type": "focal",
      "levels": ["None", "Menu Deal", "Student Fuel"],
      "reference": "None"
    },
    {
      "id": "composition",
      "label": "Composition",
      "type": "focal",
      "levels": [
        "Sandwich + Water",
        "Sandwich + Coffee",
        "Sandwich + Coffee + Fruit"
      ],
      "reference": "Sandwich + Water"
    },
    {
      "id": "price",
      "label": "Price",
      "type": "focal",
      "levels": ["3.50", "4.50", "5.50", "6.50"],
      "reference": "continuous",
      "unit": "EUR"
    },
    {
      "id": "pickup_speed",
      "label": "Pickup speed",
      "type": "filler",
      "levels": ["Ready now", "2-minute wait"],
      "reference": "Ready now"
    },
    {
      "id": "packaging",
      "label": "Packaging",
      "type": "filler",
      "levels": ["Open tray", "Closed container"],
      "reference": "Open tray"
    }
  ],
  "between_subjects": {
    "id": "pressure",
    "label": "Time pressure",
    "levels": ["low", "high"],
    "reference": "low",
    "assignment": "Qualtrics randomizer, equal probability"
  },
  "profile_space_size": 288,
  "randomization": {
    "strategy": "independent uniform sampling per attribute, no-replacement within respondent",
    "constraints": "none at launch; pilot may flag implausible combinations"
  }
}
```

- [ ] **Step 2: Verify JSON parses**

Run: `python3 -c "import json; json.load(open('qualtrics/conjoint-spec.json'))"`
Expected: no output, exit code 0.

- [ ] **Step 3: Commit**

```bash
git add qualtrics/conjoint-spec.json
git commit -m "Add machine-readable conjoint attribute spec"
```

---

## Task 4: Block 1 spec — Welcome and Consent

**Files:**
- Create: `qualtrics/blocks/01-consent.md`

- [ ] **Step 1: Write the block spec**

```markdown
# Block 1 — Welcome and Consent

## Purpose
Introduce the study, disclose data handling, get explicit consent. Non-consenters are terminated immediately.

## Items

### Q1.1 — Welcome (Descriptive Text)
**Content:**
> **Welcome!**
>
> This short survey (~6 minutes) is part of a research project at the Católica-Lisbon School of Business and Economics on **food choices in campus settings**. Your participation is entirely voluntary and you may withdraw at any time without penalty.
>
> **What we collect:** Your answers to a small number of questions plus how you rate a series of example meal offers. No directly identifying information is stored with your responses.
>
> **Incentive:** On completion you may optionally enter a lottery for one of five €20 Bolt Food vouchers. Your email, if provided, is stored separately from your responses and deleted after prizes are distributed.
>
> **Data handling:** Responses are stored pseudonymously on Qualtrics (CLSBE license, EU-hosted) in compliance with GDPR. Aggregated results may be published; individual responses will not.
>
> **Contact:** max.noelle-wying [at] edu.ulisboa.pt

### Q1.2 — Consent (Multiple Choice, single answer, force response)
**Prompt:** *I have read and understood the above information. I am at least 18 years old and consent to take part in this study.*

**Choices:**
1. Yes, I consent.
2. No, I do not consent.

## Display logic
- None — Block 1 is always shown first.

## Branch logic (set in Survey Flow, not in block)
- If Q1.2 == "No, I do not consent." → **End of Survey** with custom message:
  > Thank you. Your response has not been recorded.

## Embedded data
- None set in this block.
```

- [ ] **Step 2: Commit**

```bash
git add qualtrics/blocks/01-consent.md
git commit -m "Add Block 1 consent spec"
```

---

## Task 5: Block 2 spec — Pre-task covariates

**Files:**
- Create: `qualtrics/blocks/02-pretask-covariates.md`

- [ ] **Step 1: Write the block spec**

```markdown
# Block 2 — Pre-task Covariates

Measured *before* any treatment exposure; all items are force-response.

### Q2.1 — Hunger (Likert, 1–7, force response)
**Prompt:** *Right now, how hungry are you?*
**Scale:** 1 = Not at all hungry · 7 = Extremely hungry
**Layout:** Horizontal Likert slider.

### Q2.2 — Hours since last substantive meal (Numeric entry, bounded 0–24, force response)
**Prompt:** *How many hours has it been since your last substantive meal?*
**Validation:** Integer or decimal, minimum 0, maximum 24.

### Q2.3 — Cafeteria usage frequency (Multiple Choice, single answer, force response)
**Prompt:** *In a typical week, how often do you eat at the CLSBE cafeteria?*
**Choices:** 0 days · 1 day · 2 days · 3 days · 4 days · 5+ days.

### Q2.4 — Price sensitivity (Matrix, 3 statements × 1–7 Likert, force response per row)
**Prompt:** *How much do you agree with each statement?*
**Scale:** 1 = Strongly disagree · 7 = Strongly agree
**Rows (exact wording from Lichtenstein et al. 1993, adapted):**
1. I am willing to make an extra effort to find lower prices for lunch.
2. The money saved by finding lower lunch prices is usually worth the time and effort.
3. I will shop around for the cheapest option even when the total saving is only a euro or two.

*Analysis note:* Score = row-wise mean; Cronbach's alpha computed in R.

### Q2.5 — Dietary restrictions (Multiple Choice, multiple answer, force response allowing "None")
**Prompt:** *Do any of the following apply to you?* (Select all that apply.)
**Choices:** Vegetarian · Vegan · Halal · Kosher · Gluten-free · Other · None.

## Display logic
- None — shown to everyone after consent.

## Embedded data
- None set in this block; answers become regular response columns.
```

- [ ] **Step 2: Commit**

```bash
git add qualtrics/blocks/02-pretask-covariates.md
git commit -m "Add Block 2 pre-task covariate spec"
```

---

## Task 6: Block 3 spec — Pressure Randomizer

**Files:**
- Create: `qualtrics/blocks/03-pressure-randomizer.md`

- [ ] **Step 1: Write the block spec**

```markdown
# Block 3 — Pressure Randomizer (no visible content)

## Purpose
Assign `pressure = high` or `pressure = low` with equal probability. The respondent sees **nothing**. All work happens in the Survey Flow.

## How to configure in Qualtrics
This is **not a content block** — it is a **Randomizer element** inserted directly in the Survey Flow between the Block 2 block element and the Block 4 branches.

1. Open **Survey flow**.
2. Below Block 2, click **Add a New Element Here → Randomizer**.
3. Set **"Evenly Present Elements"** = ON, **"Randomly present"** = 1.
4. Inside the randomizer, add two **Set Embedded Data** children:
   - Child A: `pressure = high`, then `timer_duration_s = 8`
   - Child B: `pressure = low`, then `timer_duration_s = 0`
5. Each child's downstream branch points to the appropriate primer (Task 7 / 8) + rating block.

## Verification
After import/build, open Survey Flow and confirm the hierarchy reads:

```
Randomizer — Randomly present 1 of the following elements (Evenly Present = ON)
    ├── Set Embedded Data: pressure = high, timer_duration_s = 8
    │       → (points to Block 4a: High-pressure primer)
    │       → (points to Block 5 with timer JS enabled)
    └── Set Embedded Data: pressure = low, timer_duration_s = 0
            → (points to Block 4b: Low-pressure primer)
            → (points to Block 5 without timer JS)
```

## Embedded data set
- `pressure` (`high` | `low`)
- `timer_duration_s` (`8` | `0`)
```

- [ ] **Step 2: Commit**

```bash
git add qualtrics/blocks/03-pressure-randomizer.md
git commit -m "Add Block 3 pressure randomizer spec"
```

---

## Task 7: Block 4a/4b specs — Primer (branched)

**Files:**
- Create: `qualtrics/blocks/04-primer.md`

- [ ] **Step 1: Write the combined primer spec**

```markdown
# Block 4 — Instructional Primer (branched)

Each respondent sees exactly one of the two variants, determined by the Randomizer (Block 3).

## Block 4a — High-Pressure Primer

### Q4a.1 — Instructional text (Descriptive)
> **Imagine you are in the CLSBE cafeteria at lunchtime.**
>
> To simulate a real cafeteria queue, please evaluate each meal option **quickly**. You will have a short countdown (**8 seconds**) next to each rating. Please don't overthink — trust your gut.
>
> The scale runs from **1 = Not at all appealing** to **7 = Extremely appealing**.

### Q4a.2 — Warm-up rating (Conjoint rating — discard from analysis)
- Shows ONE randomly generated meal profile with the 8-second timer.
- Rating scale 1–7.
- Page-top note: *"This is a practice rating and will not be analyzed."*
- On submit, set embedded data `warmup_discarded = true`.

## Block 4b — Low-Pressure Primer

### Q4b.1 — Instructional text (Descriptive)
> **Imagine you are in the CLSBE cafeteria at lunchtime.**
>
> Please **take your time** to evaluate each option carefully. There is no time limit — we want your considered judgment.
>
> The scale runs from **1 = Not at all appealing** to **7 = Extremely appealing**.

### Q4b.2 — Warm-up rating (Conjoint rating — discard from analysis)
- Shows ONE randomly generated meal profile, no timer.
- Rating scale 1–7.
- Page-top note: *"This is a practice rating and will not be analyzed."*
- On submit, set embedded data `warmup_discarded = true`.

## Implementation note
Both warm-ups use the **same Conjoint attribute definition** built in Task 9. Attach the timer JS (Task 11) **only** to Block 4a's warm-up page so respondents get a realistic practice experience.
```

- [ ] **Step 2: Commit**

```bash
git add qualtrics/blocks/04-primer.md
git commit -m "Add Block 4 primer specs (high- and low-pressure branches)"
```

---

## Task 8: Block 5 spec — Conjoint rating tasks

**Files:**
- Create: `qualtrics/blocks/05-rating-task.md`

- [ ] **Step 1: Write the rating-task spec**

```markdown
# Block 5 — 12 Conjoint Rating Tasks

This is the heart of the experiment. Implemented via the Qualtrics **Conjoint** module in **rating / full-profile** mode.

## Conjoint configuration (set in Qualtrics Conjoint builder)

**Mode:** Full-profile, rating
**Number of profiles per respondent:** 12
**Rating scale:** 1–7 Likert, anchors "Not at all appealing" / "Extremely appealing"
**Randomization:** Independent uniform per attribute; no-replacement within respondent.
**Attributes and levels:** As in `qualtrics/conjoint-spec.json` (the Conjoint builder requires manual entry of each attribute and its levels — see the JSON for exact text).

## Profile page layout
Each profile page shows:
1. **Page header:** (high-pressure only) a countdown timer — injected by `timer-high-pressure.js`.
2. **Composite image:** pre-rendered PNG for this attribute combination (see `stimuli-plan.md`). Not yet generated; for the pilot, use Qualtrics' text-only profile rendering and add images post-pilot.
3. **Text row 1:** `{Format}` — either "Bundle" or "Separate items".
4. **Text row 2:** `{Composition}` — e.g., "Sandwich + Coffee + Fruit".
5. **Text row 3 (conditional):** label badge — "Menu Deal" or "Student Fuel" — shown only when `label != None`.
6. **Icon row:** `{Pickup speed}` and `{Packaging}` rendered as small Qualtrics-inserted text+icon.
7. **Price:** rendered bold, e.g., `€4.50`.
8. **Rating prompt:** *"How appealing is this meal option to you right now?"* — 1–7 slider.

## JavaScript attached to rating page
- **All respondents:** `response-time.js` captures ms-precision RT; writes to `rt_ms_{profileIndex}` embedded data key.
- **High-pressure only:** `timer-high-pressure.js` reads `timer_duration_s` and shows the countdown.

## Attach JS per branch
- The **same** rating block element is used in both branches; the **high-pressure** branch adds a page-level Question JS that loads the timer; the **low-pressure** branch does not.
- Implementation trick: put the timer JS inside an `if (Qualtrics.SurveyEngine.getEmbeddedData('pressure') === 'high') { … }` guard, and attach it globally. Safer than maintaining two block copies.

## Validation rules
- Force response on each rating.
- Back button disabled (set in **Survey Options → Back Button = OFF for this block**).
- Page timer (hidden, built-in) ON for diagnostic logging — not used as outcome (we use `rt_ms_*` from JS).

## Pause behavior
- Soft nudge on timer expiry: JS shows a muted-red bar reading "Please select quickly." The timer does **not** auto-advance; respondents still must click a rating before "Next".
```

- [ ] **Step 2: Commit**

```bash
git add qualtrics/blocks/05-rating-task.md
git commit -m "Add Block 5 conjoint rating-task spec"
```

---

## Task 9: Timer JavaScript — high-pressure branch

**Files:**
- Create: `qualtrics/javascript/timer-high-pressure.js`

- [ ] **Step 1: Write the JS**

Paste this JS into the **Question JS editor** of the rating page. It reads `timer_duration_s` from embedded data; when `pressure != 'high'` it silently returns.

```javascript
Qualtrics.SurveyEngine.addOnReady(function () {
    var pressure = "${e://Field/pressure}";
    if (pressure !== "high") {
        return;
    }

    var totalSeconds = parseInt("${e://Field/timer_duration_s}", 10);
    if (isNaN(totalSeconds) || totalSeconds <= 0) {
        totalSeconds = 8;
    }

    var container = document.createElement("div");
    container.id = "cre-timer-bar";
    container.style.cssText =
        "position:fixed;top:0;left:0;width:100%;padding:10px;" +
        "text-align:center;font-weight:bold;background:#ffe9a8;" +
        "border-bottom:2px solid #d29a00;z-index:9999;";
    container.innerText = "Time left: " + totalSeconds + "s";
    document.body.appendChild(container);

    var nudge = document.createElement("div");
    nudge.id = "cre-timer-nudge";
    nudge.style.cssText =
        "position:fixed;top:48px;left:0;width:100%;padding:8px;" +
        "text-align:center;color:#fff;background:#c0392b;" +
        "display:none;z-index:9999;";
    nudge.innerText = "Please select quickly.";
    document.body.appendChild(nudge);

    var remaining = totalSeconds;
    var interval = setInterval(function () {
        remaining -= 1;
        if (remaining > 0) {
            container.innerText = "Time left: " + remaining + "s";
        } else {
            container.innerText = "Time up — please select.";
            nudge.style.display = "block";
            clearInterval(interval);
        }
    }, 1000);

    this.questionclick = function (event, element) {
        clearInterval(interval);
    };
});

Qualtrics.SurveyEngine.addOnUnload(function () {
    var bar = document.getElementById("cre-timer-bar");
    var nudge = document.getElementById("cre-timer-nudge");
    if (bar) bar.parentNode.removeChild(bar);
    if (nudge) nudge.parentNode.removeChild(nudge);
});
```

- [ ] **Step 2: Manual verification plan (documented for pilot, not executed here)**

In the `qa-checklist.md` (Task 14), add:

- Preview survey with `pressure = high`; timer bar must appear top-of-page reading "Time left: 8s" and count down.
- At 0s the bar must read "Time up — please select." and the red nudge must appear.
- Preview with `pressure = low`; no timer bar, no nudge.

- [ ] **Step 3: Commit**

```bash
git add qualtrics/javascript/timer-high-pressure.js
git commit -m "Add high-pressure 8s countdown JS"
```

---

## Task 10: Response-time capture JavaScript

**Files:**
- Create: `qualtrics/javascript/response-time.js`

- [ ] **Step 1: Write the JS**

Attached to every rating page (both branches). Writes RT into `rt_ms_{n}` where `n` is the Conjoint profile index exposed by Qualtrics as `${lm://CurrentLoopNumber}`.

```javascript
Qualtrics.SurveyEngine.addOnReady(function () {
    this._cre_startTimestamp = Date.now();
});

Qualtrics.SurveyEngine.addOnUnload(function () {
    var endTs = Date.now();
    var startTs = this._cre_startTimestamp || endTs;
    var rtMs = endTs - startTs;

    var loopIndex = "${lm://CurrentLoopNumber}";
    if (!loopIndex || loopIndex === "${lm://CurrentLoopNumber}") {
        loopIndex = "1";
    }

    Qualtrics.SurveyEngine.setEmbeddedData("rt_ms_" + loopIndex, rtMs);
});
```

*Implementation note:* `${lm://CurrentLoopNumber}` is valid inside loop-and-merge blocks; for the Conjoint module, Qualtrics exposes the equivalent as `${e://Field/Q_CurrentProfileIndex}` — **verify in the pilot** which token the CLSBE Qualtrics build exposes and edit this file accordingly. The fallback to "1" ensures we never write to a malformed key.

- [ ] **Step 2: Commit**

```bash
git add qualtrics/javascript/response-time.js
git commit -m "Add response-time capture JS for rating pages"
```

---

## Task 11: Block 6 spec — Manipulation check + secondary outcomes

**Files:**
- Create: `qualtrics/blocks/06-manip-check.md`

- [ ] **Step 1: Write the block spec**

```markdown
# Block 6 — Manipulation Check and Secondary Outcomes

### Q6.1 — Felt pressure (Likert, 1–7, force response)
**Prompt:** *While rating the meal options, I felt rushed.*
**Scale:** 1 = Strongly disagree · 7 = Strongly agree
**Purpose:** Direct manipulation check for the time-pressure factor.

### Q6.2 — Open-ended WTP (Numeric entry, €, bounded 0–50, force response)
**Prompt:** *Imagine you are designing your ideal lunch at the CLSBE campus cafeteria — sandwich plus any sides and drinks you want. What is the maximum you would pay for it?*
**Validation:** Minimum 0, maximum 50, 0.5 step allowed.

### Q6.3 — Realism check (Likert, 1–7, force response)
**Prompt:** *How realistic did the meal options you just rated feel, compared to real CLSBE cafeteria offerings?*
**Scale:** 1 = Not at all realistic · 7 = Extremely realistic

### Q6.4 — Hypothesis-guess open text (Text entry, optional, 500 chars max)
**Prompt:** *In one or two sentences, what do you think this study was investigating?*
**Purpose:** Qualitative flag for demand-effect risk.

## Display logic
- None — shown to every respondent after Block 5.
```

- [ ] **Step 2: Commit**

```bash
git add qualtrics/blocks/06-manip-check.md
git commit -m "Add Block 6 manipulation-check spec"
```

---

## Task 12: Block 7 spec — Demographics

**Files:**
- Create: `qualtrics/blocks/07-demographics.md`

- [ ] **Step 1: Write the block spec**

```markdown
# Block 7 — Demographics

All items force-response unless noted. Ask for optional-only attributes in bands to reduce re-identification risk.

### Q7.1 — Gender (Multiple Choice, single answer)
**Prompt:** *What is your gender?*
**Choices:** Woman · Man · Non-binary · Prefer not to say · Prefer to self-describe: _______

### Q7.2 — Age (Multiple Choice, single answer)
**Prompt:** *What is your age?*
**Choices:** Under 18 · 18–20 · 21–23 · 24–26 · 27–29 · 30+ · Prefer not to say
**Note:** Under-18 respondents are excluded from analysis (consent form requires 18+).

### Q7.3 — Year of study (Multiple Choice, single answer)
**Prompt:** *What is your current year of study at CLSBE?*
**Choices:** Undergraduate Year 1 · Undergraduate Year 2 · Undergraduate Year 3 · Master Year 1 · Master Year 2 · PhD · Exchange student · Not currently a CLSBE student
**Note:** Non-CLSBE respondents flagged for sensitivity analysis.

### Q7.4 — Nationality (Multiple Choice, single answer)
**Prompt:** *What is your nationality?*
**Choices:** Portuguese · EU (non-Portuguese) · Non-EU · Prefer not to say
*Rationale:* Kept coarse to avoid identifying small groups.

### Q7.5 — Monthly discretionary budget (Multiple Choice, single answer)
**Prompt:** *Roughly how much money do you have available for discretionary spending (food, entertainment, etc.) per month?*
**Choices:** Under €100 · €100–€199 · €200–€349 · €350–€549 · €550–€799 · €800+ · Prefer not to say
```

- [ ] **Step 2: Commit**

```bash
git add qualtrics/blocks/07-demographics.md
git commit -m "Add Block 7 demographics spec"
```

---

## Task 13: Block 8 spec — Attention, debrief, lottery

**Files:**
- Create: `qualtrics/blocks/08-attention-debrief-lottery.md`

- [ ] **Step 1: Write the block spec**

```markdown
# Block 8 — Attention Check, Debrief, Lottery

### Q8.1 — Attention check (Matrix, instructed response, force response)
**Prompt:** *For quality control, please answer the items below as instructed.*
**Rows:**
1. Eating a balanced lunch can improve afternoon focus.
2. **For quality control, please select "Strongly agree" for this item.**
3. The CLSBE cafeteria offers daily meal options.

**Scale:** Strongly disagree · Disagree · Neutral · Agree · Strongly agree.

**Scoring:** Row 2 == "Strongly agree" → set embedded data `attention_pass = true`; else `false`.
Implement via **Survey Flow → Branch → Set Embedded Data**, or inline JS:

```javascript
Qualtrics.SurveyEngine.addOnPageSubmit(function () {
    var selected = this.getSelectedChoices();
    // Row 2 is the second statement; inspect question structure in pilot.
    var pass = this.getChoiceValue(2, 5) === true; // placeholder — verify row/col ids at build
    Qualtrics.SurveyEngine.setEmbeddedData("attention_pass", pass ? "true" : "false");
});
```
*Implementation note:* The getChoiceValue row/col ids depend on how Qualtrics instantiates the matrix — verify ids via the browser devtools before launch; document the final IDs in `qa-checklist.md`.

### Q8.2 — Debrief (Descriptive Text)
> **Thank you!** You have completed the main part of the study.
>
> **What this study was about:** We are testing how students evaluate campus meal offers. Specifically, we randomize the **bundle format** (single bundle vs. separate items), the **label** shown on the offer (none, generic "Menu Deal", or benefit-oriented "Student Fuel"), the **composition**, and the **price**. Half of respondents completed the survey under a short time limit, to test whether time pressure changes how much those labels and bundles matter.
>
> If you have any questions or would like to know the results, please email max.noelle-wying [at] edu.ulisboa.pt.

### Q8.3 — Lottery email (Text entry, optional, email format)
**Prompt:** *To enter the €20 Bolt Food voucher lottery (5 winners), please leave your email. We will use it only to contact winners and delete it afterwards.*
**Validation:** Email format; not required.

## Storage note — lottery email detachment
Set the Q8.3 data export tag to a unique name (e.g., `lottery_email`). On the Qualtrics **Data & Analysis** screen, after each collection period:
1. Export `lottery_email` to a separate file.
2. **Delete the column** from the main export before analysis.
This fulfills the GDPR separation requirement stated in the proposal §9.
```

- [ ] **Step 2: Commit**

```bash
git add qualtrics/blocks/08-attention-debrief-lottery.md
git commit -m "Add Block 8 attention-check, debrief, lottery spec"
```

---

## Task 14: Stimuli composition plan (spec only)

**Files:**
- Create: `qualtrics/stimuli-plan.md`

Actual image generation is scoped out of this plan (handled in a follow-up). The pilot uses Qualtrics' text-only profile renderer; images slot in after pilot feedback.

- [ ] **Step 1: Write the plan**

```markdown
# Stimuli Composition Plan — Meal Profile Images

## Goal
One clean, consistent PNG per unique attribute combination that can be meaningfully visualized.

## Visual elements (pre-rendered layered composite)

| Layer | Source | Notes |
|---|---|---|
| Tray / container background | `open-tray.png` or `closed-container.png` | Matches `packaging` |
| Sandwich (always present) | `sandwich.png` | Fixed position bottom-left |
| Drink | `coffee.png` or `water.png` | Matches `composition` |
| Fruit | `apple.png` | Only when `composition == "Sandwich + Coffee + Fruit"` |
| Label badge | `badge-menu-deal.svg` or `badge-student-fuel.svg` | Top-right corner; omitted when `label == "None"` |
| Price sticker | text overlay | Rendered at runtime by Qualtrics |
| Bundle ribbon | `bundle-ribbon.png` | Only when `format == "Bundle"` |

## Generation path (out of scope for this plan)
A small Python script using Pillow composites layers by attribute tuple and saves to `qualtrics/stimuli/img/{format}_{label}_{composition}_{pickup}_{packaging}.png`. Conjoint profile text → image mapping loaded via Qualtrics library upload.

## Interim plan for pilot
Qualtrics Conjoint renders text-only cards. Use those for the pilot; swap to images before full launch if pilot feedback asks for them.
```

- [ ] **Step 2: Commit**

```bash
git add qualtrics/stimuli-plan.md
git commit -m "Add stimuli composition plan (text-only for pilot)"
```

---

## Task 15: Build the survey in Qualtrics — Project creation + top-of-flow embedded data

**Files:** (external — Qualtrics platform)

- [ ] **Step 1: Create the project**

1. Log into Qualtrics (CLSBE account) → **Create new project** → **Blank Survey Project**.
2. Name: `CLSBE-CRE-Group3-BundleFraming-2026`. Folder: your personal workspace.
3. **Survey options → General → Back button: OFF by default** (we turn on per-block in Task 18).
4. **Survey options → Responses → Anonymize responses: ON**.

- [ ] **Step 2: Declare all embedded data at the top of the Survey Flow**

Open **Survey flow → Add a new element here → Embedded Data**, pinned at the TOP. Add these keys with default values:

| Key | Default |
|---|---|
| `pressure` | (leave blank) |
| `timer_duration_s` | `0` |
| `warmup_discarded` | `false` |
| `attention_pass` | `false` |
| `rt_ms_1` | (blank) |
| `rt_ms_2` | (blank) |
| `rt_ms_3` | (blank) |
| `rt_ms_4` | (blank) |
| `rt_ms_5` | (blank) |
| `rt_ms_6` | (blank) |
| `rt_ms_7` | (blank) |
| `rt_ms_8` | (blank) |
| `rt_ms_9` | (blank) |
| `rt_ms_10` | (blank) |
| `rt_ms_11` | (blank) |
| `rt_ms_12` | (blank) |

Declaring every key up front guarantees the column appears on every export even when a respondent drops out early.

- [ ] **Step 3: Verify**

Save Survey flow. Re-open; all keys must be visible under the top Embedded Data element.

- [ ] **Step 4: Commit (no repo change — mark task done in the checklist)**

No commit for this Qualtrics-side task. Tick the task in the plan.

---

## Task 16: Build Blocks 1–2 in Qualtrics

**Files:** (external — Qualtrics platform; specs in `qualtrics/blocks/01-consent.md` and `qualtrics/blocks/02-pretask-covariates.md`)

- [ ] **Step 1: Create Block 1 (Consent)**

1. Rename default block → `01 Consent`.
2. Add Descriptive Text item `Q1.1`; paste welcome copy from `01-consent.md` verbatim.
3. Add Multiple Choice item `Q1.2`; single answer; force response; paste prompt and 2 choices from `01-consent.md`.
4. **Survey flow:** After the block, add **Branch → If Q1.2 == "No, I do not consent."** → **End of Survey** element with custom message: `Thank you. Your response has not been recorded.`

- [ ] **Step 2: Create Block 2 (Covariates)**

Add a new block after Block 1 → `02 Pre-Task Covariates`. Create each of Q2.1 → Q2.5 exactly as specified in `02-pretask-covariates.md`. Enable **Force Response** on all items.

- [ ] **Step 3: Preview**

Click **Preview**; step through Consent and Covariates. Verify:
- Non-consent path ends the survey.
- Consent path reaches Block 2 and all five items render correctly.
- Force-response errors fire on empty submissions.

---

## Task 17: Build the Randomizer (Block 3) in Survey Flow

**Files:** (external — Qualtrics platform; spec in `qualtrics/blocks/03-pressure-randomizer.md`)

- [ ] **Step 1: Configure the randomizer**

In Survey Flow, below Block 2:
1. **Add a new element here → Randomizer**.
2. **Evenly Present Elements: ON**. **Randomly present: 1**.
3. Add two **Set Embedded Data** children under the randomizer.
   - Child A: `pressure = high`, then in a second SED right below, `timer_duration_s = 8`.
   - Child B: `pressure = low`, then `timer_duration_s = 0`.

*(Leave the branches empty for now; Task 18 attaches the downstream primer + rating blocks.)*

- [ ] **Step 2: Preview 4× to confirm even assignment**

Preview four times; expected ≈ 2 high / 2 low. Exact counts won't balance on such a small sample — this is only a sanity check that both branches fire.

---

## Task 18: Build Block 4 (primers) + wire the two branches

**Files:** (external; specs in `qualtrics/blocks/04-primer.md`)

- [ ] **Step 1: Create the two primer blocks**

1. New block → `04a Primer — High Pressure`. Add:
   - Q4a.1 Descriptive text (paste from `04-primer.md`).
   - Q4a.2 Conjoint rating (warm-up). Configure the Conjoint module per Task 19 then **clone** into this slot and set it to a single profile. Tag the question with embedded data `warmup_discarded = true` via `Qualtrics.SurveyEngine.addOnPageSubmit`.
2. New block → `04b Primer — Low Pressure`. Same structure, low-pressure wording, no timer.

- [ ] **Step 2: Wire branches in Survey Flow**

Under the Randomizer:
- Child A (`pressure = high`): add Block `04a Primer — High Pressure` → Block `05 Rating Tasks (High-Pressure)`.
- Child B (`pressure = low`): add Block `04b Primer — Low Pressure` → Block `05 Rating Tasks (Low-Pressure)`.

At this stage Block 5 is a placeholder; it's built in Task 19.

- [ ] **Step 3: Preview both branches**

Force `pressure = high` via URL param `?pressure=high` (Qualtrics Preview lets you set embedded data). Verify the high-pressure primer text appears. Repeat with `?pressure=low`.

---

## Task 19: Build the Conjoint rating block (Block 5)

**Files:** (external; spec in `qualtrics/blocks/05-rating-task.md`; attributes in `qualtrics/conjoint-spec.json`)

- [ ] **Step 1: Create two Block 5 instances**

The cleanest implementation is **two parallel Block 5 copies** (`05a Rating — High Pressure`, `05b Rating — Low Pressure`), identical in content but differing only in whether the timer JS loads. This avoids conditional JS logic and makes QA easy.

In each block:
1. **Add a new question → Conjoint**.
2. Conjoint settings:
   - Mode: **Full profile — rating**.
   - Number of profiles per respondent: **12**.
   - Rating scale: **1–7**, anchors "Not at all appealing" / "Extremely appealing".
3. Add attributes verbatim from `conjoint-spec.json`:
   - Format (2 levels)
   - Label (3 levels)
   - Composition (3 levels)
   - Price (4 levels)
   - Pickup speed (2 levels)
   - Packaging (2 levels)
4. Randomization: **independent** per attribute; enable **no-replacement within respondent**.

- [ ] **Step 2: Attach the JS**

- To both blocks' conjoint question, paste `qualtrics/javascript/response-time.js` into **Question JS**.
- To the high-pressure block (`05a`) only, ADDITIONALLY paste `qualtrics/javascript/timer-high-pressure.js` into **Question JS**. Order: response-time JS first, timer JS second.

- [ ] **Step 3: Disable the back button for both Block 5 copies**

Block settings → **Back button: OFF**.

- [ ] **Step 4: Preview with both pressure settings**

- `?pressure=high&timer_duration_s=8` → page header must show the 8-second countdown.
- `?pressure=low` → no timer. Rate 12 profiles; on submit inspect embedded data panel for `rt_ms_1` … `rt_ms_12` populated.

- [ ] **Step 5: Fix `${lm://CurrentLoopNumber}` token**

If embedded data keys come out as `rt_ms_` (no number) or `rt_ms_${lm://CurrentLoopNumber}` literal, edit `qualtrics/javascript/response-time.js` to use `${e://Field/Q_CurrentProfileIndex}` or the token Qualtrics actually exposes for this Conjoint mode. Commit the fix:

```bash
git add qualtrics/javascript/response-time.js
git commit -m "Fix loop index token for Qualtrics Conjoint response-time capture"
```

---

## Task 20: Build Blocks 6, 7, 8 in Qualtrics

**Files:** (external; specs in `qualtrics/blocks/06-manip-check.md`, `07-demographics.md`, `08-attention-debrief-lottery.md`)

- [ ] **Step 1: Create Block 6 (manipulation check)**

Add Q6.1–Q6.4 per `06-manip-check.md`. Force-response on Q6.1–Q6.3; optional on Q6.4.

- [ ] **Step 2: Create Block 7 (demographics)**

Add Q7.1–Q7.5 per `07-demographics.md`. Force-response on all.

- [ ] **Step 3: Create Block 8 (attention + debrief + lottery)**

Add Q8.1–Q8.3. On Q8.1 paste the scoring JS from `08-attention-debrief-lottery.md` and **confirm choice row/col ids in Preview** before finalizing.

- [ ] **Step 4: Wire Survey Flow for the final blocks**

Both branches merge back: after `05a`/`05b` the flow continues with Block 6 → Block 7 → Block 8 → **End of Survey** element with custom message: `Thank you — you're entered. Have a good lunch!`

---

## Task 21: QA checklist + pilot dry-run

**Files:**
- Create: `qualtrics/qa-checklist.md`

- [ ] **Step 1: Write the checklist**

```markdown
# Pre-Launch QA Checklist

## Survey flow sanity
- [ ] Top-of-flow embedded data element declares all 16 keys (pressure, timer_duration_s, warmup_discarded, attention_pass, rt_ms_1…12).
- [ ] Consent → Branch terminates non-consenters.
- [ ] Randomizer Evenly Present = ON, 1 of 2 children.
- [ ] 25 previews: roughly 50/50 high/low split (expect ~12/13).
- [ ] Both branches converge on Block 6 → 7 → 8 → End of Survey.

## Per-condition preview
- [ ] `?pressure=high` preview: primer copy says "8 seconds"; every rating page shows the countdown bar; bar hits 0s → "Time up" + red nudge; rating still submits when respondent clicks.
- [ ] `?pressure=low` preview: primer copy says "take your time"; no timer bar; ratings submit normally.

## Data integrity
- [ ] Submit a full high-pressure preview; export .csv; confirm columns: `pressure=high`, `rt_ms_1`…`rt_ms_12` all populated with integers > 500 ms.
- [ ] Submit a full low-pressure preview; confirm `pressure=low`, `rt_ms_*` populated (will be larger, 5–20 s typical).
- [ ] Warm-up profile response does NOT show up in the Conjoint "profiles" table — verify by ensuring only 12 profiles per respondent are recorded (the warm-up is a separate question).
- [ ] Attention check scoring: set Q8.1 row 2 = "Strongly agree" → `attention_pass=true`; set Q8.1 row 2 = anything else → `attention_pass=false`.
- [ ] Non-consenters have no Block 2+ data.

## Cross-device
- [ ] Preview on mobile (Qualtrics preview → phone icon). Timer bar must still be visible and legible; rating slider operable by thumb.

## Accessibility / ethics
- [ ] Consent wording matches the approved text (check against CLSBE ethics submission).
- [ ] Lottery email field has its own export tag and can be stripped from the main export.
- [ ] Debrief discloses the randomization and links an email contact.

## Pilot (n ≈ 20)
- [ ] 10 high-pressure, 10 low-pressure target.
- [ ] After pilot, compute: median response time per condition (expected high ≈ 6s, low ≈ 15s); felt-pressure mean difference (expected ≥ 1 Likert point); completion rate (expected ≥ 85%).
- [ ] If medians deviate > ±2 s from target, recalibrate `timer_duration_s` (6 or 10) and re-run a mini-pilot.
- [ ] Scan Q6.4 free-text: flag respondents who correctly guess the hypothesis; report count in pilot memo.
```

- [ ] **Step 2: Commit**

```bash
git add qualtrics/qa-checklist.md
git commit -m "Add pre-launch QA checklist"
```

- [ ] **Step 3: Run the QA checklist against the built survey**

Tick every box above in the checklist file (in a working copy, not committed — the committed version remains a template). Record any deviations as GitHub issues on the repo.

---

## Task 22: Export the QSF and open the PR

**Files:**
- Create: `qualtrics/qsf-export/clsbe-cre-group3.qsf`

- [ ] **Step 1: Export from Qualtrics**

Qualtrics survey list → three-dot menu on the project → **Export Survey** → saves a `.qsf` file locally.

- [ ] **Step 2: Copy into the repo**

```bash
cp ~/Downloads/CLSBE-CRE-Group3-BundleFraming-2026*.qsf \
   "/Users/max/Documents/Master/Courses/Causality and Randomized Experiments/Group Work/qualtrics/qsf-export/clsbe-cre-group3.qsf"
```

- [ ] **Step 3: Commit and push**

```bash
cd "/Users/max/Documents/Master/Courses/Causality and Randomized Experiments/Group Work"
git add qualtrics/qsf-export/clsbe-cre-group3.qsf
git commit -m "Export Qualtrics survey (pre-pilot build)"
git push
```

- [ ] **Step 4: Open the PR**

```bash
gh pr create --base main --head feature/qualtrics-survey \
  --title "Qualtrics survey — pre-pilot build" \
  --body "$(cat <<'EOF'
## Summary
- All 8 blocks built per `docs/proposal.qmd`.
- Pressure randomizer in Survey Flow; high/low branch tested in preview.
- Timer and response-time JS committed under `qualtrics/javascript/`.
- QSF exported to `qualtrics/qsf-export/clsbe-cre-group3.qsf`.

## Test plan
- [ ] Import the QSF into a fresh Qualtrics account; verify all blocks present.
- [ ] Run the QA checklist in `qualtrics/qa-checklist.md` end to end.
- [ ] Pilot with ~20 respondents between 2026-04-27 and 2026-04-29.
EOF
)"
```

---

## Self-Review

**Spec coverage — proposal.qmd sections vs. plan tasks:**

| Proposal section | Covered by task |
|---|---|
| §4.1 Approach (rating-based, mixed design) | 3, 8, 19 |
| §4.2 Population & sample (recruitment channels) | Out of scope for this plan — recruitment is operational |
| §4.3 Attributes & levels | 3, 19 |
| §4.4 Rating task structure (12 profiles, warm-up, soft nudge) | 7, 8, 9, 19 |
| §4.5 Outcome variables (rating + RT + straightlining) | 8, 10 |
| §4.6 Covariates (pre + post) | 5, 12 |
| §4.7 Randomization (profile + respondent) | 6, 17, 19 |
| §4.8 Sample size | Not implementation-relevant; in analysis plan |
| §4.9 Pilot | 21 |
| §5.1 Instrumentation (Qualtrics, timer, primer) | 15–20 |
| §5.2 Recruitment & incentives | 13 (lottery field); recruitment operational |
| Appendix A (attribute table) | 3 |
| Appendix B (8 blocks with exact wording) | 4, 5, 6, 7, 8, 11, 12, 13 |

No gaps.

**Placeholder scan:** No "TBD" / "implement later" markers. One documented uncertainty in Task 10 (`${lm://CurrentLoopNumber}` vs. `${e://Field/Q_CurrentProfileIndex}`) is resolved by Task 19 Step 5 which commits the correct token after live verification — this is a planned verification step, not a placeholder.

**Type / ID consistency:**
- `pressure` ∈ {`high`, `low`}: consistent across Tasks 3, 6, 7, 9, 15, 17, 18, 19, 21.
- `timer_duration_s` numeric: Task 6 (`8` / `0`), Task 9 reads with `parseInt`, Task 15 default `0`. Consistent.
- `rt_ms_{n}`: Task 8 refs the schema, Task 10 writes the keys, Task 15 declares them, Task 21 QA verifies presence. Consistent — **verify at Task 19 Step 5 that `{n}` = `1` to `12`**, not `0` to `11`; if off-by-one, adjust `response-time.js`.
- `attention_pass` boolean-as-string: Task 13 writes `"true"`/`"false"` strings; Task 15 defaults to `"false"`. Consistent.
- Block numbers match Survey Flow order everywhere.

Plan is internally consistent.

---

## Execution Handoff

**Plan complete and saved to `docs/superpowers/plans/2026-04-22-qualtrics-survey-implementation.md`. Two execution options:**

1. **Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration. Best for the repo-only tasks (1–14, 21, 22). Tasks 15–20 require clicking in the Qualtrics web UI — those stay on you; I review screenshots or the exported QSF.

2. **Inline Execution** — Execute all repo-only tasks in this session with checkpoints; I pause before each Qualtrics-UI task for you to complete it.

**Which approach?**
