---
description: Run ordered pipeline triage for one failed Jenkins build (agent-style workflow)
---

Act as **@pipeline-investigator** (see `.claude/agents/pipeline-investigator.md`).

1. Read and follow **`go/skills/pipeline-triage-workflow/SKILL.md`** end-to-end.
2. Ask the user only for **`JOB`** and **`BUILD`** if not already provided (e.g. `build` and `116`).
3. Execute **Stages 1–4** in order using the container commands in that skill. Do **not** pause between stages except at **GATE** or on tool failure.
4. At **GATE**, stop and wait for explicit approval before any Jira create/update or Jenkins job trigger.
5. For Jira steps after approval, use **`go/skills/pipeline-jira/SKILL.md`** or **@pipeline-handoff**.

**Example:** `/pipeline-triage` then `job build build 116`, or: ` @pipeline-investigator triage build 116 `
