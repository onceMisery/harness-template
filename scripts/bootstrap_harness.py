from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / ".harness"

REQUIRED_PATHS = [
    HARNESS / "project.json",
    HARNESS / "feature_list.json",
    HARNESS / "spec.md",
    HARNESS / "sprint_plan.json",
    HARNESS / "run_state.json",
    HARNESS / "progress.md",
]


def main() -> int:
    missing = [str(p.relative_to(ROOT)) for p in REQUIRED_PATHS if not p.exists()]
    if missing:
        print("Missing required harness files:")
        for item in missing:
            print(f"- {item}")
        return 1

    with (HARNESS / "run_state.json").open("r", encoding="utf-8") as f:
        state = json.load(f)
    print("Harness bootstrap check passed.")
    print(f"Current state: {state.get('current_state')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
