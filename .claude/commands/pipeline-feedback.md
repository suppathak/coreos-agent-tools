---
name: pipeline-feedback
description: Provide feedback on pipeline triage workflow
---

# Pipeline Feedback

Collect user feedback on any step of the pipeline triage workflow.

## Instructions

1. Read and follow `.claude/agents/pipeline-feedback-collector.md`
2. Use the `pipeline-feedback-capture` skill from `go/skills/pipeline-feedback-capture/SKILL.md`
3. Ask the user which step they want to provide feedback on (if not clear from context)
4. Collect and record their feedback

## Usage

User can invoke this after any workflow step:
- After monitoring: `/pipeline-feedback` → "The status summary was too long"
- After triage: `/pipeline-feedback` → "Root cause analysis was perfect"
- After Jira search: `/pipeline-feedback` → "Missed duplicate tickets"
- Anytime: `/pipeline-feedback` → General workflow feedback
