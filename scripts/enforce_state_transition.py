from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / ".harness/run_state.json"

ALLOWED = {
    "INIT": {"PLANNING", "FAILED"},
    "PLANNING": {"PLAN_READY", "FAILED"},
    "PLAN_READY": {"GENERATING", "FAILED"},
    "GENERATING": {"GENERATED", "FAILED"},
    "GENERATED": {"EVALUATING", "FAILED"},
    "EVALUATING": {"PASSED", "REWORK_REQUIRED", "FAILED"},
    "REWORK_REQUIRED": {"GENERATING", "FAILED"},
    "PASSED": {"GENERATING", "DONE", "FAILED"},
    "DONE": set(),
    "FAILED": set(),
}


def main() -> int:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    current = state.get("current_state")
    next_state = state.get("next_state")
    if not next_state:
        print("No next_state specified; nothing to validate")
        return 0
    if next_state not in ALLOWED.get(current, set()):
        print(f"Invalid transition: {current} -> {next_state}")
        return 1
    print(f"Valid transition: {current} -> {next_state}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
