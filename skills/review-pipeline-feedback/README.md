# Review Pipeline Feedback Skill

Search and analyze past feedback from pipeline triage workflow sessions to learn from previous experiences and improve future executions.

## Overview

This skill enables users to:
1. **Search past feedback** by step, category, text, or date range
2. **Identify patterns** in user experiences (what works, what doesn't)
3. **Learn before acting** - check feedback before using a workflow step
4. **Investigate recurring issues** - see if problems have been reported before

## Components

- **`SKILL.md`**: Defines how to use the review skill
- **`scripts/search_feedback.py`**: Python script for searching and filtering feedback

## Data Source

Reads from: `skills/pipeline-feedback-capture/scripts/feedback.json`

This is the same file where `/pipeline-feedback` stores all feedback entries.

## Usage

### Via Agent
```
@pipeline-feedback-reviewer
"What did people say about pipeline-monitor?"
```

### Via Slash Command
```
/review-feedback pipeline-investigator
```

### Direct Script Usage
```bash
# Show all feedback
python skills/review-pipeline-feedback/scripts/search_feedback.py

# Filter by step
python skills/review-pipeline-feedback/scripts/search_feedback.py --step pipeline-monitor

# Filter by category
python skills/review-pipeline-feedback/scripts/search_feedback.py --category Complexity

# Search for text
python skills/review-pipeline-feedback/scripts/search_feedback.py --search "build #116"

# Recent feedback only
python skills/review-pipeline-feedback/scripts/search_feedback.py --days 7

# Combine filters
python skills/review-pipeline-feedback/scripts/search_feedback.py \
  --step pipeline-investigator \
  --category Accuracy \
  --days 30

# Summary only (no individual entries)
python skills/review-pipeline-feedback/scripts/search_feedback.py --summary-only

# Limit results
python skills/review-pipeline-feedback/scripts/search_feedback.py --limit 10
```

## Search Filters

| Filter | Description | Example |
|--------|-------------|---------|
| `--step` | Pipeline workflow step | `pipeline-monitor`, `pipeline-investigator` |
| `--category` | Feedback category | `Complexity`, `Clarity`, `Accuracy`, `Positive` |
| `--search` | Text search (feedback, context, notes) | `"build #116"`, `"verbose"` |
| `--days` | Feedback from last N days | `7`, `30` |
| `--summary-only` | Show stats only, not individual entries | (flag) |
| `--limit` | Limit number of results | `5`, `10` |

## Output Format

### Summary Section
- Total entries found
- Breakdown by step
- Breakdown by category

### Individual Entries (unless --summary-only)
For each matching entry:
- Date and session ID
- Step and category
- User
- Feedback text
- Optional note
- Context (what happened)

## Use Cases

### 1. Before Using a Workflow Step
**Question:** "I'm about to use @pipeline-monitor, what should I expect?"

**Search:** `--step pipeline-monitor`

**Result:** See past user experiences, common complaints, positive feedback

**Action:** Adjust expectations, prepare for known issues

---

### 2. Investigating Recurring Failures
**Question:** "Build #116 keeps failing, has this been seen before?"

**Search:** `--search "116"`

**Result:** Find any feedback mentioning build #116

**Action:** Learn from previous investigations, avoid duplicating work

---

### 3. Understanding Patterns
**Question:** "What do users complain about most?"

**Search:** `--summary-only` (then drill into top categories)

**Result:** See which categories have most entries

**Action:** Focus improvements on high-feedback areas

---

### 4. Checking Recent Issues
**Question:** "Any recent feedback I should know about?"

**Search:** `--days 7`

**Result:** Last week's feedback

**Action:** Stay current with latest user experiences

---

### 5. Evaluating Specific Aspects
**Question:** "Is the pipeline-investigator accurate?"

**Search:** `--step pipeline-investigator --category Accuracy`

**Result:** All accuracy-related feedback for investigator

**Action:** Understand reliability before relying on triage results

## Example Output

```
Loaded 4 total feedback entries from:
  /Users/supathak/CoreOS/coreos-agent-tools/skills/pipeline-feedback-capture/scripts/feedback.json

================================================================================
FEEDBACK SUMMARY — 2 entries found
================================================================================

By Step:
  pipeline-investigator: 2

By Category:
  Complexity: 1
  Accuracy: 1

================================================================================
INDIVIDUAL ENTRIES
================================================================================
Entry #1 — 22-April-2026
================================================================================
Step:     pipeline-investigator
Category: Accuracy
User:     supathak
Session:  manual_20260422_180018

Feedback:
  The root cause analysis was spot on!

Note:
  This saved me 30 minutes of manual log reading

Context:
  Triaged build #116, classified as infra flake, identified network timeout

================================================================================
Entry #2 — 22-April-2026
================================================================================
Step:     pipeline-investigator
Category: Complexity
User:     supathak
Session:  manual_20260422_180110

Feedback:
  The log analysis was great, but it showed 50 lines of logs which was too much

Note:
  Maybe 10-15 lines would be enough to understand the issue

Context:
  Investigated recent pipeline failure, analyzed console logs, classified failure as infra flake
```

## Integration with Workflow

### Feedback Loop Cycle

1. **Capture** → User provides feedback via `/pipeline-feedback`
2. **Store** → Feedback saved to `feedback.json`
3. **Review** → User searches feedback via `/review-feedback`
4. **Learn** → User adjusts approach based on past experiences
5. **Improve** → Workflow becomes more effective over time

### Suggested Workflow

**Before starting work:**
```
/review-feedback {step-you-plan-to-use}
```

**During investigation:**
```
/review-feedback --search "{error or build number}"
```

**After completion:**
```
/pipeline-feedback  # Add your own feedback to help future users
```

## Design Principles

- **Read-only** - This skill never modifies feedback, only reads it
- **Fast** - Searching JSON is quick, results appear instantly
- **Flexible** - Multiple filter options for different use cases
- **Informative** - Summary + details give both overview and depth
- **Actionable** - Results help users make better decisions

## Future Enhancements

Potential additions:
- **Trend analysis** - Track feedback over time
- **Sentiment scoring** - Quantify positive vs. negative feedback
- **Automatic insights** - ML-based pattern detection
- **Export** - Generate reports from feedback data
- **Integration** - Link feedback to Jira tickets or build numbers

For now, the skill provides solid foundation for learning from past experiences.
