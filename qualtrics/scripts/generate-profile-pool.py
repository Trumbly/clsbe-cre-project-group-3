"""Generate the deterministic full-factorial profile pool for the rating-based
conjoint study. Reads attribute levels from ``qualtrics/conjoint-spec.json``
and writes every attribute combination (2 x 3 x 3 x 4 x 2 x 2 = 288 rows) to
``qualtrics/profiles/profile-pool.csv``.

No randomness: running this script twice produces byte-identical output.
Per-respondent randomization of 12 profiles out of 288 is done by Qualtrics
Loop & Merge at runtime.
"""

from __future__ import annotations

import csv
import itertools
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


def main() -> None:
    spec = json.loads(SPEC_PATH.read_text())
    attrs = {a["id"]: a["levels"] for a in spec["attributes"]}

    columns = [
        "ProfileID", "Format", "Label", "Composition",
        "Price", "PickupSpeed", "Packaging", "ImageURL",
    ]

    combos = list(itertools.product(
        attrs["format"],
        attrs["label"],
        attrs["composition"],
        attrs["price"],
        attrs["pickup_speed"],
        attrs["packaging"],
    ))

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(columns)
        for i, (fmt, lab, comp, price, pickup, pack) in enumerate(combos, start=1):
            w.writerow([
                f"P{i:03d}", fmt, lab, comp, price, pickup, pack,
                image_url(comp),
            ])

    print(f"Wrote {len(combos)} profiles to {OUT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
