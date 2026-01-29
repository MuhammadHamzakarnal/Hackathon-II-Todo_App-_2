---
id: 0001
title: Analysis Abort Missing Prerequisites
stage: general
date: 2026-01-16
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: user
command: /sp.analyze
labels: ["analysis", "prerequisites", "abort"]
links:
  spec: specs/hackathon-phase-ii/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - history/prompts/general/0001-analysis-abort-missing-prerequisites.general.prompt.md
tests:
  - null
---

## Prompt

User invoked `/sp.analyze` command without arguments.

## Response snapshot

Analysis could not proceed due to missing prerequisites. Found `spec.md` at `specs/hackathon-phase-ii/spec.md` but `plan.md` and `tasks.md` are missing. Instructed user to run `/sp.plan` followed by `/sp.tasks` before re-running `/sp.analyze`.

## Outcome

- ✅ Impact: None - analysis aborted due to missing files
- 🧪 Tests: N/A
- 📁 Files: Only PHR created
- 🔁 Next prompts: /sp.plan, /sp.tasks, then /sp.analyze
- 🧠 Reflection: Prerequisites check correctly identified missing artifacts

## Evaluation notes (flywheel)

- Failure modes observed: Missing plan.md and tasks.md required for cross-artifact analysis
- Graders run and results (PASS/FAIL): N/A - prerequisite check
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
