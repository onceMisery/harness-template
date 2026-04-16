# Harness Architecture

## Goal

Turn project delivery into a controlled loop:

1. Planner expands requirements into executable artifacts.
2. Generator implements the current approved sprint only.
3. Evaluator validates output against contracts and quality gates.
4. Orchestration advances or returns the sprint based on result.

## Layers

- **Orchestration**: entrypoint, sequencing, retries, state transition
- **Planner**: specification, feature decomposition, sprint planning
- **Generator**: scoped implementation and handoff
- **Evaluator**: testing, scoring, verdict
- **Runtime memory**: `.harness/` as the persistent operating state

## Core invariants

- Do not skip planning.
- Do not run critical flow in background mode.
- Do not implement features outside the current sprint contract.
- Do not mark completion outside `feature_list.json`.
