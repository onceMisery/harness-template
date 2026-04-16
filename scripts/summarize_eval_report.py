from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / ".harness/evaluator_reports"


def main() -> int:
    files = sorted(REPORTS.glob("*.json"))
    if not files:
        print("No evaluator reports found")
        return 0
    for report_path in files:
        data = json.loads(report_path.read_text(encoding="utf-8"))
        print(
            f"{report_path.name}: verdict={data.get('verdict')} "
            f"score={data.get('score')} blockers={len(data.get('blockers', []))}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
