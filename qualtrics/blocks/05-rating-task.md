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
