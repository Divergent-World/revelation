import csv

from paths import PUBLISHING


MANIFEST = PUBLISHING / "historical-book-build" / "PLATE_MANIFEST.csv"
VALID_STATUSES = {"survives", "fragmentary", "missing_or_lost", "unknown"}


def load_statuses():
    with MANIFEST.open(newline="", encoding="utf-8-sig") as source:
        statuses = {
            row["slot_id"]: row["historical_status"]
            for row in csv.DictReader(source)
        }
    if len(statuses) != 90 or set(statuses.values()) - VALID_STATUSES:
        raise ValueError(f"invalid plate status manifest: {MANIFEST}")
    return statuses
