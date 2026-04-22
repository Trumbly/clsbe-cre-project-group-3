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
