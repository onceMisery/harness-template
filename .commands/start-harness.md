You are starting the harness workflow for: $ARGUMENTS

Run in order:
1. Initialize required `.harness/` files if missing.
2. Start planner.
3. When planner finishes, inspect `.harness/sprint_plan.json`.
4. Start generator for the current sprint.
5. Start evaluator after generator finishes.
6. If evaluator returns REWORK_REQUIRED, return to generator.
7. If all features in `.harness/feature_list.json` have `passes=true`, mark DONE.

Constraints:
- No background execution for critical steps.
- Update `run_state.json` and `progress.md` on every transition.
