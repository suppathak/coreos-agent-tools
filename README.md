# CoreOS Agent Tools

CLI tools for monitoring and analyzing Red Hat CoreOS (RHCOS) infrastructure.

## Tools

| Tool | Description |
|------|-------------|
| `coreos_pipeline_messages.py` | Fetch Slack messages from CoreOS pipeline channels |
| `jenkins.py` | Manage Jenkins jobs, builds, queue, and nodes |
| `process_rhcos_cves.py` | Process RHCOS CVEs from Jira and match with RHEL issues |
| `get_rhcos_image.py` | Retrieve RHCOS container image data for OCP versions |

## Quick Start

```bash
# Build container
podman build -t quay.io/cverna/coreos-agent-tools .

# Run with environment variables
podman run --rm --env-file .env quay.io/cverna/coreos-agent-tools <script> [options]
```

See `CLAUDE.md` for detailed usage examples and environment variable configuration.

## Go CLI

A Go implementation is available in the `go/` directory:

```bash
cd go
go build -o bin/coreos-tools ./cmd/coreos-tools
./bin/coreos-tools --help
```

## Claude Code integration

### Pipeline status (legacy)

Copy `coreos_pipeline_status.md` to `~/.claude/commands/` to use `/coreos_pipeline_status`.

### Agentic pipeline POC (`feature/pipeline-triage-workflow`)

This branch adds **ordered triage**, **named agents**, and **slash commands** for RHCOS Jenkins workflows. Full behavior is documented in **`CLAUDE.md`**.

**Prerequisites**

- [Claude Code](https://claude.ai/code) installed
- Podman (or Docker) and a `.env` with `JENKINS_URL`, `JENKINS_USER`, `JENKINS_API_TOKEN` (see `CLAUDE.md`)

**Setup (once per machine)**

```bash
# 1. Build the tools image (re-run after Dockerfile or script changes)
podman build -t quay.io/cverna/coreos-agent-tools .

# 2. Install slash commands for Claude Code
mkdir -p ~/.claude/commands
cp .claude/commands/pipeline-status.md ~/.claude/commands/
cp .claude/commands/pipeline-triage.md ~/.claude/commands/
# Optional: legacy pipeline summary
cp coreos_pipeline_status.md ~/.claude/commands/   # if you use /coreos_pipeline_status
```

**Run Claude Code** from the repo root (`claude`), then:

| Action | What to type |
|--------|----------------|
| Pipeline health / what to triage | `/pipeline-status` or ask: *What’s the current RHEL CoreOS Jenkins pipeline status?* |
| Deep triage for one build | `/pipeline-triage` then *job `build`, build `116`* — or `@pipeline-investigator triage job build, build 116` |
| Jira draft (no auto-create) | `@pipeline-handoff` with your triage summary |
| Next-step options | `@remediation-advisor` after triage |
| Group failures by root cause | `@cross-build-analyst` (see `.claude/agents/cross-build-analyst.md`) |

**Repo layout for agents**

- `.claude/agents/*.md` — personas (monitor, investigator, handoff, remediation, cross-build analyst)
- `go/skills/pipeline-triage-workflow/SKILL.md` — staged workflow (Gather → Logs → Classify → Summarize → human **GATE** before Jira/reruns)
- `go/skills/pipeline-failures`, `pipeline-jira`, etc. — domain playbooks the agents reference

`~/.claude/commands/` only registers slash commands; **source files stay in this repo** so the team can review them in PRs.