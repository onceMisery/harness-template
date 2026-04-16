# Harness Template Pack

A repository-ready template pack for using a planner / generator / evaluator harness in backend, web, and fullstack projects.

## What is included

- `.harness/`: runtime memory, schemas, sprint contracts, reports
- `.agents/`: role prompts and boundaries
- `.skills/`: reusable operating rules
- `.commands/`: orchestration entry prompts
- `scripts/`: bootstrap and validation helpers
- `docs/`: architecture and best-practice notes
- `apps/web/`: suggested web app layout
- `apps/backend/`: suggested backend service layout
- `tests/`: shared test layers
- `ci/`: starter CI and quality gate files

## Suggested usage

1. Copy the whole template into a repo.
2. Edit `.harness/project.json` to match your stack and target.
3. Fill `spec.md`, `feature_list.json`, and `sprint_plan.json`.
4. Use `.commands/start-harness.md` as the orchestration entry.
5. Enforce the JSON schemas in `.harness/schemas/` through CI.
6. Keep `run_state.json` and `progress.md` updated on every transition.

## Minimal startup path

- Planning: `.commands/plan-project.md`
- Sprint delivery: `.commands/run-sprint.md`
- Evaluation: `.commands/evaluate-sprint.md`
- Closeout: `.commands/close-project.md`

## Runtime invariants

- `.harness/feature_list.json` is the only source of truth for feature completion.
- All critical steps must run serially.
- No sprint may advance before evaluator approval.
- The project is only complete when all features have `passes=true`.
