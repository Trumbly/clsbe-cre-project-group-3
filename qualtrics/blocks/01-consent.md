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
