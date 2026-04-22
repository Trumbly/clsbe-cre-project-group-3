"""Generate a deterministic balanced 48-row profile pool for the rating-based
conjoint study. Reads attribute levels from ``qualtrics/conjoint-spec.json``
and writes the pool to ``qualtrics/profiles/profile-pool.csv``.

Design
------
The pool is constructed via a blocked Latin-square-style cycle to guarantee:
  * Marginal balance on every attribute (each level appears equally often).
  * Orthogonality on the Format x Label interaction (every Format x Label
    combination appears 8 times) -- needed to identify H5.
  * Near-balance on Format x Composition (every combination appears 8 times).

Per-respondent randomization of 12 profiles out of 48 is handled by Qualtrics
Loop & Merge at runtime (Randomize loop order = ON, Present only = 12).

Balance summary
---------------
  Format       : 24 | 24
  Label        : 16 | 16 | 16
  Composition  : 16 | 16 | 16
  Price        : 12 | 12 | 12 | 12
  PickupSpeed  : 24 | 24
  Packaging    : 24 | 24
  Format x Label : 8 per cell (exact)
  Format x Composition : 8 per cell (exact)

No randomness -- running this script twice produces byte-identical output.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = REPO_ROOT / "qualtrics" / "conjoint-spec.json"
OUT_PATH = REPO_ROOT / "qualtrics" / "profiles" / "profile-pool.csv"

IMG_BASE = (
    "https://raw.githubusercontent.com/Trumbly/clsbe-cre-project-group-3/"
    "feature/qualtrics-survey/qualtrics/stimuli/img"
)
COMPOSITION_TO_FILENAME = {
    "Sandwich + Water": "sandwich-water.png",
    "Sandwich + Coffee": "sandwich-coffee.png",
    "Sandwich + Coffee + Fruit": "sandwich-coffee-fruit.png",
}


def image_url(composition: str) -> str:
    fn = COMPOSITION_TO_FILENAME[composition]
    return f"{IMG_BASE}/{fn}"


def build_rows(attrs: dict[str, list[str]]) -> list[list[str]]:
    fmt_levels = attrs["format"]
    lab_levels = attrs["label"]
    comp_levels = attrs["composition"]
    price_levels = attrs["price"]
    pickup_levels = attrs["pickup_speed"]
    packaging_levels = attrs["packaging"]

    rows: list[list[str]] = []
    profile_num = 1
    for fmt_i in range(len(fmt_levels)):
        for lab_i in range(len(lab_levels)):
            cell_idx = fmt_i * len(lab_levels) + lab_i
            for k in range(8):
                comp_i = (cell_idx + k) % len(comp_levels)
                price_i = k % len(price_levels)
                pickup_i = k % len(pickup_levels)
                pack_i = (k // 2) % len(packaging_levels)
                rows.append([
                    f"P{profile_num:03d}",
                    fmt_levels[fmt_i],
                    lab_levels[lab_i],
                    comp_levels[comp_i],
                    price_levels[price_i],
                    pickup_levels[pickup_i],
                    packaging_levels[pack_i],
                    image_url(comp_levels[comp_i]),
                ])
                profile_num += 1
    return rows


def main() -> None:
    spec = json.loads(SPEC_PATH.read_text())
    attrs = {a["id"]: a["levels"] for a in spec["attributes"]}

    columns = [
        "ProfileID", "Format", "Label", "Composition",
        "Price", "PickupSpeed", "Packaging", "ImageURL",
    ]

    rows = build_rows(attrs)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(columns)
        w.writerows(rows)

    print(f"Wrote {len(rows)} profiles to {OUT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
