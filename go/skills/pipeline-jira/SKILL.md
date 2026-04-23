---
name: pipeline-jira
description: Create JIRA issues for CI pipeline failures - COS project conventions and subtask structure
---

# Pipeline JIRA

JIRA CLI commands and COS project conventions for tracking CI pipeline failures.

> Related: `pipeline-failures`  
> Use whatever **Jira tools** the session provides (CLI and/or MCP); the **JQL** below is the same either way.

## JIRA CLI Commands

### Listing Issues

```bash
# List issues with JQL query
jira issue list --project COS --type Task -q "summary ~ 'Pipeline Monitoring'" --plain

# List open issues
jira issue list --project COS --status "Open" --plain

# List issues by component
jira issue list --project COS --component RHCOS --plain
```

### Similar issues (bounded search)

Use this **before** drafting a **new** ticket when you have **job name**, **build**, and a **short error or classification** (often from triage). Keep result sets small; widen the window only if needed.

**Principles:** default **COS**, **last 7 days** (`updated`), **open / in progress** first; add **text** or **summary** terms from the failure; use `jira issue view KEY` to compare.

**Browse URLs:** When listing similarity candidates (dedupe), include a **clickable browse URL** per issue key: `https://<JIRA_HOST>/browse/<KEY>`. Derive `<JIRA_HOST>` from your Jira base URL / MCP config (e.g. `redhat.atlassian.net`, `issues.redhat.com`); do not output only the REST `self` URL without a `/browse/<KEY>` link.

```bash
# Recent COS activity (adjust -7d → -14d only if needed)
jira issue list --project COS -q "updated >= -7d ORDER BY updated DESC" --plain

# Open or in progress only (parentheses matter for OR)
jira issue list --project COS -q "updated >= -7d AND (statusCategory = \"To Do\" OR statusCategory = \"In Progress\") ORDER BY updated DESC" --plain

# Narrow: job name in summary (replace build with real job token)
jira issue list --project COS -q "updated >= -7d AND summary ~ 'build' ORDER BY updated DESC" --plain

# Narrow: free-text token from logs (quote special JQL characters)
jira issue list --project COS -q "updated >= -7d AND text ~ 'registry' ORDER BY updated DESC" --plain
```

JQL support varies slightly by Jira site; if a query fails, simplify (e.g. drop `statusCategory`, use `status in (Open, \"In Progress\")` per your workflow).

### Creating Issues

```bash
# Create a sub-task
jira issue create --type Sub-task --parent <PARENT-KEY> --project COS \
  --summary "<job> #<build-number> - <stream> <brief-description>" \
  --label <label> \
  --body "<detailed-markdown-description>" --no-input

# Create a task
jira issue create --type Task --project COS \
  --summary "<summary>" \
  --body "<description>" --no-input
```

### Managing Issues

```bash
# Add a comment
jira issue comment add <ISSUE-KEY> "<comment-text>" --no-input

# View issue details
jira issue view <ISSUE-KEY>

# Transition issue status
jira issue move <ISSUE-KEY> "In Progress"
```

## COS Project Conventions

### Project: COS

The COS project is used for CoreOS-related issues.

### Pipeline Monitoring Tasks

Weekly Pipeline Monitoring tasks track CI failures:

```bash
# Find current week's monitoring task
jira issue list --project COS --type Task -q "summary ~ 'Pipeline Monitoring'" --plain
```

### Sub-task Structure

Each build failure should be its own sub-task (including retries that failed).

**Summary format:**
```
<job> #<build-number> - <stream> <brief-description>
```

**Examples:**
- `build #3456 - rhel-9.6 kernel regression in selinux test`
- `build-arch #1234 - c9s compose failure - repo timeout`
- `release #789 - rhel-9.8 extensions-container build failed`

### Sub-task Body Structure

```markdown
## Build Details
- **Job**: <job-name>
- **Build**: #<build-number>
- **Stream**: <stream>
- **Timestamp**: <timestamp>
- **Duration**: <duration>
- **Jenkins URL**: <url>

## Root Cause Analysis
<description of what caused the failure>

## Error Messages
```
<error messages in code blocks>
```

## Resolution
- **Status**: <resolved/unresolved/retry-pending>
- **Retry Build**: #<retry-build-number> (if applicable)
- **Fix PR**: <link> (if applicable)
```

## Labels

| Label | When to Use |
|-------|-------------|
| `flake-infrastructure` | Transient infrastructure issues (repo timeouts, GitHub 500, network) |
| `flake-test` | Flaky test failures (passed on rerun) |
| `bug` | Actual bugs requiring code fixes |

## Issue Linking

For CVE tracking, link OCPBUG issues to RHEL vulnerability issues:

```bash
# Links are created via API, type: "Blocks"
# OCPBUG blocks RHEL (outward)
# RHEL is blocked by OCPBUG (inward)
```
