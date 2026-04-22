# Stimuli Composition Plan — Meal Profile Images

## Goal
One clean, consistent PNG per unique attribute combination that can be meaningfully visualized.

## Visual elements (pre-rendered layered composite)

| Layer | Source | Notes |
|---|---|---|
| Tray / container background | `open-tray.png` or `closed-container.png` | Matches `packaging` |
| Sandwich (always present) | `sandwich.png` | Fixed position bottom-left |
| Drink | `coffee.png` or `water.png` | Matches `composition` |
| Fruit | `apple.png` | Only when `composition == "Sandwich + Coffee + Fruit"` |
| Label badge | `badge-menu-deal.svg` or `badge-student-fuel.svg` | Top-right corner; omitted when `label == "None"` |
| Price sticker | text overlay | Rendered at runtime by Qualtrics |
| Bundle ribbon | `bundle-ribbon.png` | Only when `format == "Bundle"` |

## Generation path (out of scope for this plan)
A small Python script using Pillow composites layers by attribute tuple and saves to `qualtrics/stimuli/img/{format}_{label}_{composition}_{pickup}_{packaging}.png`. Conjoint profile text → image mapping loaded via Qualtrics library upload.

## Interim plan for pilot
Qualtrics Conjoint renders text-only cards. Use those for the pilot; swap to images before full launch if pilot feedback asks for them.
