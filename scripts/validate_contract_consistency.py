from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEATURES = ROOT / ".harness/feature_list.json"
SPRINT = ROOT / ".harness/sprint_plan.json"


def main() -> int:
    features = {item["id"] for item in json.loads(FEATURES.read_text(encoding="utf-8"))}
    plan = json.loads(SPRINT.read_text(encoding="utf-8"))
    for sprint in plan.get("sprints", []):
        for fid in sprint.get("feature_ids", []):
            if fid not in features:
                print(f"Unknown feature in sprint plan: {fid}")
                return 1
    print("Sprint plan references known features only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
