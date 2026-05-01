# Skills (Claude playbooks)

Each subdirectory is a **skill**: typically **`SKILL.md`** plus optional scripts or **`README.md`**.

These files are **documentation and workflow instructions** for Claude Code / OpenCode — **not** Go source code (the Go CLI lives in **`../go/`**).

**Consumption**

- **Claude Code:** `.claude/agents/*.md` points here (e.g. `skills/pipeline-triage-workflow/SKILL.md`).
- **OpenCode agent image:** `go/Dockerfile.agent` copies this tree to `/opt/opencode-skills/` at build time.

**Adding a skill:** create `skills/<short-name>/SKILL.md` with frontmatter (`name`, `description`) consistent with other skills, then reference it from the relevant agent.
