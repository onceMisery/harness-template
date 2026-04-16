# Harness Core Skill

## Purpose
Define the shared operating rules of the harness runtime.

## Rules
1. `.harness/feature_list.json` is the only source of truth for feature completion.
2. Every critical transition must update `.harness/run_state.json`.
3. Every critical transition must append `.harness/progress.md`.
4. The flow is serial: planner -> generator -> evaluator.
5. Do not run critical steps in background mode.
6. No sprint may advance without evaluator approval.
7. The project is complete only when all features have `passes=true`.
