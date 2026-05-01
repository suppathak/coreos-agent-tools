---
name: pipeline-feedback-capture
description: Ask user if they would like to provide feedback. Call scripts/formatting.py. Don't ask any follow up questions.
allowed-tools:
  - write
  - read
  - bash
---

# Pipeline Feedback Capture

Step 1 [Claude] Ask user if they would like to provide feedback.
Step 2 [Claude] IF the user provides feedback, select a feedback category that best suits feedback
Step 3 [Claude] Summarize user feedback as users-feedback, and summarize what happened as context.
Step 4 [Claude] Ask if user has any additional notes/comments (optional)
Step 5 [Claude] You MUST run scripts/formatting.py \
  --category {Category} \
  --step {Pipeline step name} \
  --feedback {users-feedback} \
  --context {Summary of what happened, include what you did, explain your output quickly} \
  --note {Optional additional note/comment from user, if provided}

## Usage
1. Never provide the user with options for feedback categories
2. Whatever comment they provide assume that's the feedback
3. After getting feedback, ask simply: "Any additional notes?" (don't ask if they already provided extra context)
4. You MUST use scripts/formatting.py

## Feedback format
Take the comment the user gave as feedback and create the following inputs for scripts/formatting.py and you must call scripts/formatting.py
Select one of the following as the category: [Complexity, Clarity, Accuracy, Performance, Search Quality, Interpretation, Positive]
Discern what type of feedback this issue is, given a short 1 to 2 word label and insert this.
Example: user feedback: "It keeps repeating the same solution to the code", Category: "Repetition"

Run: python scripts/formatting.py \
  --category {Category} \
  --step {Pipeline step - e.g., "pipeline-monitor", "pipeline-investigator", "jira-similarity-search"} \
  --feedback {users-feedback} \
  --context {Summary of what happened, include what you did, explain your output quickly} \
  --note {Optional note/comment - only include if user provided one}

## Pipeline Steps
Common step names:
- pipeline-monitor
- pipeline-investigator
- jira-similarity-search
- pipeline-handoff
- remediation-advisor
- cross-build-analyst
- general-workflow
