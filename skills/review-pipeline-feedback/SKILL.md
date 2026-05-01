---
name: review-pipeline-feedback
description: Search and review past pipeline feedback to learn from previous experiences
allowed-tools:
  - read
  - bash
---

# Review Pipeline Feedback

Search and review past feedback from pipeline triage workflow sessions to learn from previous user experiences, identify patterns, and avoid known issues.

## When to Use

- **Before starting a workflow step** - "What did people think of pipeline-monitor?"
- **Investigating recurring issues** - "Has build #116 been mentioned before?"
- **Understanding patterns** - "What are common complaints about the investigator?"
- **Learning from past sessions** - "Any feedback about duplicate detection?"

## How to Use

Step 1 [Claude] Understand what the user wants to review (step, category, text search, time range)
Step 2 [Claude] Run scripts/search_feedback.py with appropriate filters
Step 3 [Claude] Present findings in a clear, actionable format
Step 4 [Claude] Optionally suggest insights or patterns observed

## Script Usage

```bash
# Show all feedback
python scripts/search_feedback.py

# Filter by step
python scripts/search_feedback.py --step pipeline-monitor

# Filter by category
python scripts/search_feedback.py --category Complexity

# Search for text
python scripts/search_feedback.py --search "build #116"

# Recent feedback (last 7 days)
python scripts/search_feedback.py --days 7

# Combine filters
python scripts/search_feedback.py --step pipeline-investigator --category Accuracy

# Just show summary
python scripts/search_feedback.py --summary-only

# Limit results
python scripts/search_feedback.py --step pipeline-monitor --limit 5
```

## Available Filters

**--step**: Filter by workflow step
- pipeline-monitor
- pipeline-investigator
- jira-similarity-search
- pipeline-handoff
- remediation-advisor
- cross-build-analyst
- general-workflow

**--category**: Filter by feedback category
- Complexity
- Clarity
- Accuracy
- Performance
- Search Quality
- Interpretation
- Positive

**--search**: Search text in feedback, context, and notes

**--days**: Show feedback from last N days

**--summary-only**: Show only statistics, not individual entries

**--limit**: Limit number of results

## Output Interpretation

The script shows:
1. **Summary** - Count by step and category
2. **Individual entries** - Full details of each matching feedback

Use this information to:
- Understand user sentiment about workflow steps
- Identify recurring issues or patterns
- Learn from past successes (Positive feedback)
- Avoid known problems before they occur

## Important Notes

- This skill is **read-only** - it reviews past feedback, doesn't modify it
- Feedback is stored in: `skills/pipeline-feedback-capture/scripts/feedback.json`
- Empty results mean no matching feedback exists yet
- Use `--summary-only` for quick overviews, full output for details
