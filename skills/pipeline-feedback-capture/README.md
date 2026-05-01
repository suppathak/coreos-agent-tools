# Pipeline Feedback Capture Skill

Collect and persist user feedback on pipeline triage workflow steps.

## Overview

This skill allows the agent to:
1. **Ask** the user for feedback on any workflow step
2. **Categorize** feedback (Complexity, Clarity, Accuracy, Performance, Search Quality, Interpretation, Positive)
3. **Summarize** the context of what happened
4. **Record** structured feedback to `feedback.json`

## Components

- **`SKILL.md`**: Defines the agent's behavior and script invocation
- **`scripts/formatting.py`**: Python script that appends feedback entries to `feedback.json`

## Usage

Invoked via:
- `@pipeline-feedback-collector` agent
- `/pipeline-feedback` slash command
- Manual skill invocation

## Feedback Storage

All feedback is appended to: `skills/pipeline-feedback-capture/scripts/feedback.json`

Each entry contains:
```json
{
  "id": "session_id_or_timestamp",
  "category": "Accuracy",
  "date": "22-April-2026",
  "timestamp": "2026-04-22T09:15:30.123456",
  "step": "pipeline-investigator",
  "feedback": "The root cause analysis was spot on!",
  "context": "Investigated build #116, classified as infra flake, identified network timeout",
  "note": "This would have taken me 30 minutes manually",
  "user": "username",
  "source": "pipeline-feedback-capture"
}
```

**Note:** The `note` field is optional and only included if the user provides additional comments.

## Workflow Steps

Common step names:
- `pipeline-monitor` - Discovery and health checks
- `pipeline-investigator` - Triage and root cause analysis
- `jira-similarity-search` - Duplicate detection
- `pipeline-handoff` - Ticket creation and routing
- `remediation-advisor` - Remediation suggestions
- `cross-build-analyst` - Multi-build analysis
- `general-workflow` - Overall experience

## Script Arguments

```bash
python scripts/formatting.py \
  --category "Accuracy" \
  --step "pipeline-investigator" \
  --feedback "The root cause was correct" \
  --context "Analyzed build #116, found network timeout" \
  --note "This saved me 20 minutes"  # Optional
```

**Required arguments:**
- `--category`: Feedback category (see below)
- `--step`: Pipeline workflow step
- `--feedback`: User's feedback text
- `--context`: Summary of what happened

**Optional arguments:**
- `--note`: Additional notes or comments from user

## Categories

- **Complexity** - Too complex, overwhelming, or too simple
- **Clarity** - Clear or confusing communication
- **Accuracy** - Correctness of analysis/results
- **Performance** - Speed, efficiency, time to insight
- **Search Quality** - Relevance of search/discovery results
- **Interpretation** - Understanding of context, intent, requirements
- **Positive** - General positive feedback
