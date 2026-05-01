#!/usr/bin/env python3
"""Search and review past pipeline feedback entries."""

import argparse
import json
from pathlib import Path
from datetime import datetime, timedelta


def load_feedback(feedback_file):
    """Load feedback entries from JSON file."""
    if not feedback_file.exists():
        print(f"No feedback file found at {feedback_file}")
        return []

    try:
        with open(feedback_file) as f:
            data = json.load(f)
            if not isinstance(data, list):
                print("Warning: feedback.json is not a list")
                return []
            return data
    except Exception as e:
        print(f"Error reading feedback file: {e}")
        return []


def filter_by_step(entries, step):
    """Filter entries by pipeline step."""
    if not step:
        return entries
    return [e for e in entries if e.get("step", "").lower() == step.lower()]


def filter_by_category(entries, category):
    """Filter entries by category."""
    if not category:
        return entries
    return [e for e in entries if e.get("category", "").lower() == category.lower()]


def filter_by_date_range(entries, days):
    """Filter entries from last N days."""
    if not days:
        return entries

    cutoff = datetime.now() - timedelta(days=days)
    filtered = []

    for e in entries:
        try:
            entry_date = datetime.fromisoformat(e.get("timestamp", ""))
            if entry_date >= cutoff:
                filtered.append(e)
        except Exception:
            # Include entries with invalid/missing timestamps
            continue

    return filtered


def search_text(entries, query):
    """Search for text in feedback, context, and note fields."""
    if not query:
        return entries

    query_lower = query.lower()
    filtered = []

    for e in entries:
        # Search in feedback, context, and note fields
        searchable = " ".join([
            e.get("feedback", ""),
            e.get("context", ""),
            e.get("note", "")
        ]).lower()

        if query_lower in searchable:
            filtered.append(e)

    return filtered


def format_entry(entry, index):
    """Format a single entry for display."""
    lines = []
    lines.append(f"\n{'='*80}")
    lines.append(f"Entry #{index + 1} — {entry.get('date', 'Unknown date')}")
    lines.append(f"{'='*80}")
    lines.append(f"Step:     {entry.get('step', 'N/A')}")
    lines.append(f"Category: {entry.get('category', 'N/A')}")
    lines.append(f"User:     {entry.get('user', 'N/A')}")
    lines.append(f"Session:  {entry.get('id', 'N/A')}")
    lines.append(f"\nFeedback:")
    lines.append(f"  {entry.get('feedback', 'N/A')}")

    if entry.get('note'):
        lines.append(f"\nNote:")
        lines.append(f"  {entry['note']}")

    lines.append(f"\nContext:")
    lines.append(f"  {entry.get('context', 'N/A')}")

    return "\n".join(lines)


def format_summary(entries):
    """Format a summary of all entries."""
    if not entries:
        return "\nNo feedback entries found."

    lines = []
    lines.append(f"\n{'='*80}")
    lines.append(f"FEEDBACK SUMMARY — {len(entries)} entries found")
    lines.append(f"{'='*80}")

    # Count by step
    steps = {}
    for e in entries:
        step = e.get('step', 'Unknown')
        steps[step] = steps.get(step, 0) + 1

    lines.append("\nBy Step:")
    for step, count in sorted(steps.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"  {step}: {count}")

    # Count by category
    categories = {}
    for e in entries:
        cat = e.get('category', 'Unknown')
        categories[cat] = categories.get(cat, 0) + 1

    lines.append("\nBy Category:")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"  {cat}: {count}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Search and review past pipeline feedback.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Show all feedback
  python search_feedback.py

  # Show feedback for a specific step
  python search_feedback.py --step pipeline-monitor

  # Show feedback by category
  python search_feedback.py --category Complexity

  # Show feedback from last 7 days
  python search_feedback.py --days 7

  # Search for specific text
  python search_feedback.py --search "build #116"

  # Combine filters
  python search_feedback.py --step pipeline-investigator --category Accuracy

  # Just show summary
  python search_feedback.py --summary-only
        """
    )

    parser.add_argument(
        "--step",
        help="Filter by pipeline step (e.g., pipeline-monitor, pipeline-investigator)"
    )
    parser.add_argument(
        "--category",
        help="Filter by category (Complexity, Clarity, Accuracy, Performance, etc.)"
    )
    parser.add_argument(
        "--days",
        type=int,
        help="Show feedback from last N days"
    )
    parser.add_argument(
        "--search",
        help="Search for text in feedback, context, and notes"
    )
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="Show only summary statistics, not individual entries"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of results shown"
    )
    parser.add_argument(
        "--feedback-file",
        type=Path,
        default=None,
        help="Path to feedback.json file (default: auto-detect)"
    )

    args = parser.parse_args()

    # Determine feedback file path
    if args.feedback_file:
        feedback_file = args.feedback_file
    else:
        # Default to the pipeline-feedback-capture location
        script_dir = Path(__file__).parent
        feedback_file = script_dir / "../../pipeline-feedback-capture/scripts/feedback.json"
        feedback_file = feedback_file.resolve()

    # Load all feedback
    entries = load_feedback(feedback_file)

    if not entries:
        print("\nNo feedback entries found.")
        return 0

    print(f"\nLoaded {len(entries)} total feedback entries from:")
    print(f"  {feedback_file}")

    # Apply filters
    entries = filter_by_step(entries, args.step)
    entries = filter_by_category(entries, args.category)
    entries = filter_by_date_range(entries, args.days)
    entries = search_text(entries, args.search)

    # Apply limit
    if args.limit:
        entries = entries[:args.limit]

    # Show summary
    print(format_summary(entries))

    # Show individual entries unless summary-only
    if not args.summary_only and entries:
        print("\n" + "="*80)
        print("INDIVIDUAL ENTRIES")
        for i, entry in enumerate(entries):
            print(format_entry(entry, i))

    print(f"\n{'='*80}\n")

    return 0


if __name__ == "__main__":
    exit(main())
