# Harness Best Practices

## Planning

- Every feature must have a stable ID.
- Every feature must have acceptance criteria.
- Every sprint must define allowed and forbidden changes.
- Out-of-scope items must be explicit.

## Generation

- Implement only the current sprint.
- Add tests with every feature.
- Write a handoff before evaluation.
- Update progress and runtime state every loop.

## Evaluation

- Use blocker / major / minor issue levels.
- Fail fast on blocker issues.
- Keep the scoring rubric stable across sprints.
- Stop after the configured maximum rework rounds.

## Governance

- Enforce schemas in CI.
- Archive evaluation reports and test artifacts.
- Record key decisions in `decisions.md`.
- Record recurring project risks in `risks.md`.
