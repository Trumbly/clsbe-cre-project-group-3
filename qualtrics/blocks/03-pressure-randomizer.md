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
