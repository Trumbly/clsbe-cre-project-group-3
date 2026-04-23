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
> **What this study was about:** We are testing how students evaluate campus meal offers. Specifically, we randomize the **bundle format** (single bundle vs. separate items), the **label** shown on the offer (none, generic "Menu Deal", or benefit-oriented "Student Deal"), the **composition**, and the **price**. Half of respondents completed the survey under a short time limit, to test whether time pressure changes how much those labels and bundles matter.
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
