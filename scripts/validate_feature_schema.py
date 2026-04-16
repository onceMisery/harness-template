from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEATURE_PATH = ROOT / ".harness/feature_list.json"

REQUIRED_KEYS = {
    "id", "name", "module", "type", "priority", "status", "passes",
    "dependencies", "acceptance_criteria", "test_scope", "owner",
    "last_eval_score", "notes"
}


def main() -> int:
    data = json.loads(FEATURE_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        print("feature_list.json must be an array")
        return 1

    for idx, item in enumerate(data, start=1):
        missing = REQUIRED_KEYS - set(item.keys())
        if missing:
            print(f"Feature #{idx} missing keys: {sorted(missing)}")
            return 1
    print("feature_list.json basic validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
