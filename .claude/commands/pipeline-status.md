---
description: RHCOS Jenkins pipeline health — use Pipeline Monitor agent
---

You are running **`/pipeline-status`**. This is **mandatory routing** per root `CLAUDE.md`.

1. **Read** `.claude/agents/pipeline-monitor.md`.
2. Execute that agent’s playbook: discover failing / relevant Jenkins jobs (main **`build`** job and peers as the skill implies), pick the **best triage target** if appropriate.
3. Output using the **Pipeline Monitor — Summary** format from that file.
4. End with a clear handoff: **@pipeline-investigator** or **`/pipeline-triage`** with job + build when the user wants deep triage.

Use `podman` + `.env` + `quay.io/cverna/coreos-agent-tools` and `jenkins.py` as in `CLAUDE.md`.
