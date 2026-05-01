---
name: pipeline-triage-workflow
description: Ordered agent-style triage for a single failed Jenkins build — gather metadata, logs, classification, summary; human gate before Jira writes. Jira search is a separate agent.
---

# Pipeline triage workflow (agentic)

Run **one failed build** through a **fixed sequence** of stages. Each stage has a **single job** and **structured output** for the next. Do **not** stop between stages for “what next?” — only at **GATE** unless blocked by errors.

> **Container:** All Jenkins commands use the image from `CLAUDE.md` (rebuild before runs):
> `podman build -t quay.io/cverna/coreos-agent-tools .`
>
> **Shorthand** (replace `.env` path if needed):
> ```bash
> RUN="podman run --rm --env-file .env quay.io/cverna/coreos-agent-tools"
> ```

**Inputs (required):** `JOB` (Jenkins job name), `BUILD` (integer build number).

**Related skills:** `pipeline-failures` (deep patterns, kola via `coreos-tools` if you use the Go image), `pipeline-jira` (COS Jira **after** GATE), `pipeline-gitlab` (internal **GitLab** failure tracker; PAT + API), **`@pipeline-handoff`** for drafts.

**Multi-agent sequence (recommended):** **@pipeline-investigator** (this skill, stages 1–4) → **@gitlab-similarity-search** (read-only GitLab history / flake cache; `skills/pipeline-gitlab`) → **@jira-similarity-search** (read-only COS Jira; `skills/pipeline-jira`) → **@pipeline-handoff** (draft). Investigator does **not** call Jira or GitLab; keep Jenkins vs tracker concerns separate.

**Why GitLab before Jira:** Team convention — **GitLab** holds **historical / recurring** failure notes with low notification noise; **Jira** is for **actionable** COS work. Check the internal tracker **first**, then COS Jira for duplicates and parents. Skip GitLab only if **`GITLAB_TOKEN`** / **`glab`** is unavailable (say so at GATE).

---

## Stage 1 — Gather (build metadata)

**Agent role:** Collect facts about the failing build.

**Run:**
```bash
$RUN jenkins.py builds info JOB BUILD --pretty
$RUN jenkins.py jobs info JOB --pretty
```

**Output (write this block before Stage 2):**

```markdown
### Gather
- **Job:** …
- **Build:** …
- **Status / result:** …
- **Stream / parameters (if any):** …
- **URL:** …
```

---

## Stage 2 — Logs (console evidence)

**Agent role:** Pull console log and extract high-signal lines.

**Run:**
```bash
$RUN jenkins.py builds log JOB BUILD --pretty
```

If the log is huge, re-run and capture tail locally (host):
```bash
$RUN jenkins.py builds log JOB BUILD --pretty 2>&1 | tail -n 200
```

**Output:**

```markdown
### Logs (excerpt)
- **Last ~N lines or key errors:** …
- **Patterns seen** (error / timeout / registry / test): …
```

Use grep patterns from `pipeline-failures` when analyzing saved log text (`error:`, `FATAL:`, `timeout`, `unauthorized`, `FAILED`, etc.).

**Optional (Go toolchain only):** If you run the **`coreos-tools`** Jenkins CLI from the Go build, add kola summary per `pipeline-failures`:
`coreos-tools jenkins builds kola-failures JOB BUILD --pretty`

---

## Stage 3 — Classify

**Agent role:** Map the failure to a **single primary** category and note confidence.

**Categories (pick one primary):** `infrastructure` | `flake` | `test_regression` | `package_change` | `registry_auth` | `tooling` | `unknown`

**Rules of thumb:**
- Transient network / GitLab / “try rerun” language → **flake** or **infrastructure**
- `unauthorized` pulling images → **registry_auth**
- Kola `rerun_failed: true` (if you have kola output) → **test_regression** / **package_change** per `pipeline-failures`
- Only flakes on rerun → do **not** treat as sole root cause; look for compose errors in log

**Output:**

```markdown
### Classify
- **Primary:** …
- **Confidence:** low | medium | high
- **Why (1–3 bullets):** …
```

---

## Stage 4 — Summarize (triage conclusion)

**Agent role:** Produce the **handoff package** for humans (and later Jira).

**Output:**

```markdown
### Triage summary
- **One-line summary:** …
- **Evidence:** build URL, log pointers
- **Suggested next steps:** (e.g. rerun / open COS subtask / escalate to RHEL / snooze test — **suggest only**)
- **Related downstream jobs to check:** e.g. `build-arch` if `build` failed (see `pipeline-failures`)
```

---

## GATE — Human checkpoint (no Jira / no rerun without approval)

**Stop.** Present **Gather → Logs → Classify → Summarize** to the user.

**Next agents (typical order):** Tell the user to run **@gitlab-similarity-search** first (when **`GITLAB_TOKEN`** or **`glab`** is available), then **@jira-similarity-search**, with job, build, classification, and a short error excerpt **before** **@pipeline-handoff**, so **historical GitLab** context precedes **actionable Jira** dedupe.

**Default policy:** Only **suggest** Jira / GitLab text or rerun. Do **not** run `jira issue create`, GitLab issue create, or `jenkins.py jobs build` unless the user **explicitly** asks. Do **not** query Jira or GitLab from this skill—use the **similarity** agents for that.

After similarity + approval, use **`pipeline-jira`** / **`pipeline-gitlab`** with **@pipeline-handoff** for conventions and commands.

---

## Execution rules for Claude Code

1. Complete **Stages 1–4 in order** in one run when the user provides `JOB` and `BUILD`.
2. Ask for **JOB** and **BUILD** only if missing; do not ask “what next?” between stages **1–4**.
3. On CLI errors (auth, network), stop and report; do not invent build data.
4. Prefer **`jenkins.py`** (Python container) for portability; use **`coreos-tools`** only when that binary is available in the user’s environment.
