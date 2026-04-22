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
