---
id: 001
title: Update constitution with provided content
stage: constitution
date: 2026-01-16
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: 3tee
command: /sp.constitution
labels: ["constitution", "governance", "principles"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - specs/features/task-crud.md
tests:
  - ---
---

## Prompt

/sp.constitution
 update
## Project
Hackathon Phase II: Todo Full-Stack Web Application

## Core Principles
- **Accuracy:** All API, frontend, backend, and database implementations must match the specs exactly.
- **Clarity:** Code and components should be easy to understand for any developer reviewing the project.
- **Reproducibility:** Every feature must work consistently in both local and deployed environments.
- **Rigor:** Security and authentication (JWT + Better Auth) must follow best practices.
If you need anything, feel free to ask!Pher: Frontend and backend should be optimized, avoiding unnecessary computations and slow rendering.

## Key Standards
- All API endpoints must follow the spec: `GET /api/{user_id}/tasks`, `POST`, `PUT`, `DELETE`, `PATCH` as defined.
- Database schema must enforce user-task ownership and data integrity.
- JWT token handling must be correct for all authenticated endpoints.
- Frontend UI must be responsive, modular, and reusable.
- Animations should enhance UX, not distract.
- Security: No plain text passwords, JWTs expire, and Better Auth secret must be consistent.

## Constraints
- Use only technologies defined in the spec: Next.js 16+, FastAPI, SQLModel, Neon Serverless PostgreSQL.
- All tasks and authentication features must be fully implemented before moving to additional features.
- All prompts, tasks, and specs must be handled via Claude Code—no manual coding.
- Mobile-first design for all UI components.

## Success Criteria
- All five basic features implemented correctly (Task CRUD + Auth).
- Only task owner can view or modify their tasks.
- Frontend, backend, and database fully integrated and functional.
- No JWT or auth bypass possible.
- UI matches spec and is responsive across devices.
- Application passes performance checks and does not have rendering or computation bottlenecks.

## Response snapshot

Updated project constitution from template to version 1.0.0 with five core principles: Accuracy, Clarity, Reproducibility, Rigor, and Performance.

Added Key Standards, Constraints, and Success Criteria sections specific to the Todo Full-Stack Web Application project.

Created task CRUD feature specification at specs/features/task-crud.md with six user stories and detailed API requirements.

## Outcome

- ✅ Impact: Established governance framework for Todo application development
- 🧪 Tests: No tests run - constitution documents principles
- 📁 Files: Updated constitution.md, created task-crud.md
- 🔁 Next prompts: /sp.plan for task-crud feature, /sp.tasks for implementation tasks
- 🧠 Reflection: Successfully converted user principles into structured constitution and feature spec

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not applicable
- Prompt variant (if applicable): Not applicable
- Next experiment (smallest change to try): Test constitution compliance check in next planning phase