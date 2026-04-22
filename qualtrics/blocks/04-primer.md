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
