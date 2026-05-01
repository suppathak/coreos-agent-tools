---
name: pipeline-gitlab
description: Search and manage GitLab issues for pipeline failure history — PAT + API, bounded queries, browse URLs (no MCP required)
---

# Pipeline GitLab

Use the **internal GitLab project** for **historical / flake-style** failures (per team agreement: **Jira** = human action; **GitLab** = durable record and dedupe signal). In the **recommended workflow**, run **GitLab similarity before Jira similarity** so the internal tracker is checked **first**. This skill uses the **GitLab REST API** with a **Personal Access Token** (or **`glab`** after `glab auth login`). **GitLab MCP is optional**; many self-managed instances block OAuth scopes—in that case this skill is the supported path.

**Default project (override with env):** `coreos/pipeline-failure-tracker` on `https://gitlab.cee.redhat.com`.

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GITLAB_TOKEN` | Yes (for `curl`) | Personal access token with at least **`read_api`** (add **`read_repository`** if your org requires it for issue visibility). |
| `GITLAB_HOST` | No | API host **without** path, e.g. `gitlab.cee.redhat.com` (no `https://`). |
| `GITLAB_PROJECT` | No | URL-encoded or raw path: `coreos/pipeline-failure-tracker` (slashes become `%2F` in URLs). |

Never commit tokens. Use shell `export`, a **gitignored** `.env`, or a password manager—not the repo. (This repo’s **`.gitignore`** already ignores **`.env`**.)

**TLS:** If `curl` fails with certificate errors on corporate GitLab, use your org CA bundle (`SSL_CERT_FILE` / `CURL_CA_BUNDLE`) or the same PEM approach you use for Node (`NODE_EXTRA_CA_CERTS` does not apply to `curl` unless you point `CURL_CA_BUNDLE` at it).

### Claude Code: why `GITLAB_TOKEN` is “missing” in Bash

Claude Code’s **Bash** tool often runs in a **subprocess that does not inherit** variables you exported only in the terminal **before** starting `claude`. Putting secrets in **`.env`** at the **repository root** fixes that—as long as you **load `.env` inside the same command** as `curl` / `glab`.

**Always** prefix GitLab API commands with (run from **`coreos-agent-tools` repo root**):

```bash
set -a
[ -f .env ] && . ./.env
set +a
```

Then use **`GITLAB_HOST`**, **`GITLAB_PROJECT`**, **`GITLAB_TOKEN`** as usual. **Never** echo or log token values.

If `.env` lives elsewhere, use an absolute path: `. /path/to/coreos-agent-tools/.env` (same `set -a` / `set +a` pattern).

**One-liner** (registry search example — adjust `search=`):

```bash
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)" && set -a && [ -f .env ] && . ./.env && set +a && \
  ENC="${GITLAB_PROJECT:-coreos/pipeline-failure-tracker}" && ENC="${ENC//\//%2F}" && \
  curl -sS --header "PRIVATE-TOKEN: ${GITLAB_TOKEN}" \
  "https://${GITLAB_HOST:-gitlab.cee.redhat.com}/api/v4/projects/${ENC}/issues?search=registry&per_page=5&state=all"
```

Add to **`.env`** (same file as Jenkins):

```bash
GITLAB_HOST=gitlab.cee.redhat.com
GITLAB_PROJECT=coreos/pipeline-failure-tracker
GITLAB_TOKEN=glpat-your-token-here
# Optional for corporate TLS:
# CURL_CA_BUNDLE=/path/to/your-ca-bundle.pem
```

## Browse URLs (required for each candidate)

For every issue you list as a similarity candidate, include a **web URL**:

`https://<GITLAB_HOST>/<project_path>/-/issues/<iid>`

Example: `https://gitlab.cee.redhat.com/coreos/pipeline-failure-tracker/-/issues/12`

Use **`iid`** (project issue number) from the API JSON, not necessarily the global `id`.

## Similar issues (bounded search)

**Principles:** Keep **`per_page` small** (e.g. **5–10**). Prefer **narrow `search` terms** (job name token, distinctive error substring). Widen only if empty. Prefer **recent** issues (`order_by=updated_at&sort=desc`).

**Cross-links to Jira:** If an issue body or title references **`COS-####`**, mention it in your summary so humans see both systems.

### curl (no extra tools)

Set **`GITLAB_TOKEN`** in the shell (or use `glab` auth). **`PROJECT_ENC`** is the project path with **`/` → `%2F`** (Bash: `${GITLAB_PROJECT//\//%2F}`).

```bash
export GITLAB_HOST="${GITLAB_HOST:-gitlab.cee.redhat.com}"
export GITLAB_PROJECT="${GITLAB_PROJECT:-coreos/pipeline-failure-tracker}"
PROJECT_ENC="${GITLAB_PROJECT//\//%2F}"

# Recent issues (bounded)
curl -sS --header "PRIVATE-TOKEN: ${GITLAB_TOKEN}" \
  "https://${GITLAB_HOST}/api/v4/projects/${PROJECT_ENC}/issues?per_page=10&order_by=updated_at&sort=desc&state=all"

# Narrow: free-text search (job name or error token)
curl -sS --header "PRIVATE-TOKEN: ${GITLAB_TOKEN}" \
  "https://${GITLAB_HOST}/api/v4/projects/${PROJECT_ENC}/issues?search=registry&per_page=5&state=all"

# Single issue by iid (replace IID)
curl -sS --header "PRIVATE-TOKEN: ${GITLAB_TOKEN}" \
  "https://${GITLAB_HOST}/api/v4/projects/${PROJECT_ENC}/issues?iids[]=IID"
```

Pipe JSON through **`jq`** for readable fields (`title`, `state`, `iid`, `web_url`, `description`).

### glab (optional)

After one-time auth: `glab auth login --hostname gitlab.cee.redhat.com --token "$GITLAB_TOKEN"`

```bash
export GITLAB_HOST="${GITLAB_HOST:-gitlab.cee.redhat.com}"
export GITLAB_PROJECT="${GITLAB_PROJECT:-coreos/pipeline-failure-tracker}"
ENC="${GITLAB_PROJECT//\//%2F}"

glab api "projects/${ENC}/issues?search=build&per_page=5&state=all" --hostname "$GITLAB_HOST"
```

## Creating or updating issues (explicit human ask only)

Only when the user **clearly** asks to create or comment in this session (reuse **`GITLAB_HOST`**, **`GITLAB_PROJECT`**, **`PROJECT_ENC`** from the `curl` examples above):

```bash
# Create issue (example — adjust title/body)
curl -sS --request POST --header "PRIVATE-TOKEN: ${GITLAB_TOKEN}" \
  --header "Content-Type: application/json" \
  --data '{"title":"…","description":"…"}' \
  "https://${GITLAB_HOST}/api/v4/projects/${PROJECT_ENC}/issues"
```

Prefer **GitLab UI** or **`glab issue create`** if the user already uses `glab`; keep automation aligned with team policy (noise vs Jira).

## Related

- **`pipeline-jira`** — COS Jira dedupe and actionable work.
- **`.claude/agents/gitlab-similarity-search.md`** — read-only dedupe persona and **`### Similar GitLab check`** output contract.
