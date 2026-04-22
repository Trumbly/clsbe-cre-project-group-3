# CRE Spring 2026 — Group Project

**Topic:** The Bundle Effect in Campus Food Service — A Rating-Based Conjoint Experiment with Time-Pressure Moderation

## Files

- `proposal.qmd` — Main proposal document. Open in RStudio, render to PDF.
- `references.bib` — BibTeX bibliography (22 entries, all cited in the proposal).
- `apa.csl` — (optional) APA citation style file. Download from https://github.com/citation-style-language/styles if needed.

## To render

```bash
quarto render proposal.qmd
```

Or in RStudio: open `proposal.qmd` → Render button.

Requires: Quarto, TinyTeX or a LaTeX distribution.

## Design summary

- **6 attributes** randomized per profile: 4 focal (Format, Label, Composition, Price) + 2 filler (Pickup speed, Packaging).
- **Rating-based** full-profile conjoint — 1–7 appeal rating, 12 profiles per respondent.
- **Time pressure** randomized at respondent level: half with 8-second countdown timer, half self-paced.
- **Target n = 200** CLSBE students (100 per pressure condition) = 2,400 total rating observations.
- **Primary model:** linear mixed-effects (lme4), respondent random intercepts, focal × pressure interactions.
- **WTP:** coefficient / price-coefficient ratio, bootstrapped CIs, cross-validated against open-ended WTP.

## Status

- [x] Part I — Experiment Design (complete draft, revised after professor feedback)
- [ ] Part II — Implementation (filled in after data collection, May 5 onwards)
- [ ] Part III — Analysis and Discussion (filled in after analysis, May 8 onwards)

## Revision log

- **v0.1** — initial CBC (choice-based) draft
- **v0.2** — switched to rating-based per professor feedback; added time-pressure between-subjects factor; added 2 filler attributes (pickup speed, packaging); added H7; revised analysis plan to mixed-effects linear regression; 7 new references (Rao 2014, Petty & Cacioppo 1986, Chaiken 1980, Dhar & Nowlis 1999, Payne et al. 1988, Suri & Monroe 2003, Orme 2010).

## Open decisions / to-do before Qualtrics build

1. Final price points — confirm €3.50–€6.50 range matches actual CLSBE cafeteria prices.
2. Exact timer duration for high-pressure condition — 8 s is a placeholder; pilot will calibrate (target median RT ≈ 6 s under pressure).
3. Warm-up task content — decide what profile to use for the discarded warm-up rating.
4. Author last names in YAML header.
5. Recruitment channels — which WhatsApp/Telegram groups, which courses to ask.
6. Lottery incentive value — €20 × 5 Bolt Food vouchers vs. alternatives.
7. Stimuli production — who photographs / composes the meal images (Carmen as lead).

## Next synchronous meeting agenda

- Review v0.2 proposal incorporating professor feedback.
- Lock attribute levels and stimuli design.
- Assign team roles formally.
- Begin Qualtrics build (target ready for pilot by April 28).
- Set recruitment kickoff for April 30.
