---
name: review-feedback
description: Review past pipeline workflow feedback
---

# Review Pipeline Feedback

Search and analyze past feedback from pipeline triage workflow sessions.

## Instructions

1. Read and follow `.claude/agents/pipeline-feedback-reviewer.md`
2. Use the `review-pipeline-feedback` skill from `skills/review-pipeline-feedback/SKILL.md`
3. Determine what the user wants to search for
4. Run the search with appropriate filters
5. Present insights clearly and concisely

## Usage

Quick searches:
- `/review-feedback` → Show all feedback
- `/review-feedback pipeline-monitor` → Feedback on a specific step
- `/review-feedback accuracy` → Feedback by category
- `/review-feedback "build #116"` → Text search

The agent will:
- Parse your intent
- Search the feedback database
- Show relevant entries and patterns
- Provide actionable insights

## Common Questions

- "What did people think of X?" → Filter by step
- "Has this been seen before?" → Text search
- "Any recent complaints?" → Filter by days
- "What's most problematic?" → Summary view

## Behind the Scenes

Searches: `skills/pipeline-feedback-capture/scripts/feedback.json`

All feedback from `/pipeline-feedback` invocations is stored there and searchable.
