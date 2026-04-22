# Block 5 — 12 Rating Tasks (Loop & Merge design)

Original plan assumed the Qualtrics **Conjoint** module. The CLSBE license does
not expose the Conjoint question type, so the rating task is implemented via
**Loop & Merge** over a deterministic, fully-balanced profile pool.

## Profile pool

- `qualtrics/profiles/profile-pool.csv` — 288 rows, full factorial of the six
  attributes. Generated deterministically by
  `qualtrics/scripts/generate-profile-pool.py`; no randomness, reproducible.
- Columns: `ProfileID`, `Format`, `Label`, `Composition`, `Price`,
  `PickupSpeed`, `Packaging`.

The pool is fully balanced: every attribute level appears equally often, and
every pair of attribute levels appears equally often. Drawing 12 rows uniformly
at random from this pool preserves the identification assumptions of
Hainmueller et al. (2014) for rating-based conjoint: attribute levels are
independent across draws and uniformly distributed.

## Two parallel block copies

Create two blocks in Qualtrics, identical except for the timer JS:

- `05a Rating — High Pressure` — timer JS attached.
- `05b Rating — Low Pressure` — no timer JS.

Both are wired into the respective pressure branches in the Survey Flow.

## Loop & Merge configuration (per block)

1. Open block `05a` → **Block options → Loop & Merge**.
2. Enable Loop & Merge.
3. **Loop based on a fixed number of iterations: 12** (Qualtrics will sample
   without replacement from the loop source when combined with Step 4).
4. **Loop source: CSV**. Upload `qualtrics/profiles/profile-pool.csv`.
   Map fields in this order (field indices are referenced in the question body
   via `${lm://Field/N}`):
   - Field 1 → `ProfileID`
   - Field 2 → `Format`
   - Field 3 → `Label`
   - Field 4 → `Composition`
   - Field 5 → `Price`
   - Field 6 → `PickupSpeed`
   - Field 7 → `Packaging`

   The image URL is **not** a CSV column — it is injected at runtime by
   `javascript/inject-composition-image.js`, which picks the PNG based on two
   fields (Field 4 = Composition, Field 7 = Packaging):

   | Packaging | Composition | Image |
   |---|---|---|
   | Open tray | Sandwich + Water | `sandwich-water.png` |
   | Open tray | Sandwich + Coffee | `sandwich-coffee.png` |
   | Open tray | Sandwich + Coffee + Fruit | `sandwich-coffee-fruit.png` |
   | Closed container | Sandwich + Water | `closed-container-water.png` |
   | Closed container | Sandwich + Coffee | `closed-container-coffee.png` |
   | Closed container | Sandwich + Coffee + Fruit | `closed-container-coffee.png` |

   (Fruit fits inside the closed container, so the two coffee variants share
   one image.) Keeping URLs out of the CSV avoids redundant storage and keeps
   the Qualtrics L&M grid fast to save.
5. **Randomize loop order:** ON — Qualtrics draws 12 distinct rows per
   respondent in random order.
6. **Present only:** 12 (of 288).

Repeat for block `05b`.

## Rating question inside the loop (single question per block)

Add ONE Slider question (Likert 1–7) per block. The question body displays
the current profile's attributes via piped loop-merge fields.

**Question body** — render as rich text (HTML mode):

```
<p><strong>Meal option ${lm://Field/1}</strong></p>
<p>Format: ${lm://Field/2}<br>
Composition: ${lm://Field/4}<br>
Label: ${lm://Field/3}<br>
Pickup speed: ${lm://Field/6}<br>
Packaging: ${lm://Field/7}</p>
<p><strong>Price: €${lm://Field/5}</strong></p>
<p><em>How appealing is this meal option to you right now?</em></p>
```

The image is prepended to this block at runtime by
`javascript/inject-composition-image.js`.

If "Label: None" reads awkwardly, add a small JS snippet to hide that line
when the value is "None":

```javascript
Qualtrics.SurveyEngine.addOnReady(function () {
    var labelVal = "${lm://Field/3}";
    if (labelVal === "None") {
        var qText = this.getQuestionContainer().querySelector(".QuestionText");
        if (qText) qText.innerHTML = qText.innerHTML.replace(/Label: None<br>\s*/, "");
    }
});
```

**Scale:** Slider, 1–7, labels "Not at all appealing" (1) and "Extremely
appealing" (7). Force response ON.

## Question JavaScript attached

Both blocks attach, in this order:

1. `javascript/inject-composition-image.js` — reads Field 4 and prepends the
   composition image.
2. `javascript/response-time.js` — captures per-profile RT. Loop & Merge
   exposes the current iteration as `${lm://CurrentLoopNumber}`.

Block `05a` additionally attaches `javascript/timer-high-pressure.js` after
the two shared scripts. Timer behavior is unchanged from the original spec.

## Block options

- **Back button:** OFF (per-block setting). Prevents retroactive rating edits
  under time pressure.

## Why this is equivalent to Conjoint for identification

- Attribute levels are independently and uniformly distributed across the 288
  profiles by construction.
- "Random order, 12 iterations, no replacement within respondent" reproduces
  the same per-respondent sampling distribution that the Conjoint module would
  have produced.
- No carryover: each respondent sees 12 profiles drawn independently of other
  respondents.
- The analysis model (lmer with respondent random intercepts, attribute-level
  dummies) is identical to what the proposal specifies.

The only loss compared to native Conjoint: no pre-registered orthogonal design
matrix. We substitute a fully balanced full-factorial pool, which is actually
stronger on balance.

## Data export

Each rating produces one cell per respondent × iteration. Loop & Merge
prefixes the question name per iteration, e.g. `1_QID<n>` through
`12_QID<n>`. Reshape to long format in R before analysis; join on `ProfileID`
to recover attribute values.
