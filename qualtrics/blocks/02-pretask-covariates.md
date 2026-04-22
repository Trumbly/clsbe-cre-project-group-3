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
