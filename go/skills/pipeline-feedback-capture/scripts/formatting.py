#!/usr/bin/env python3
"""Pipeline feedback capture - simplified version for CoreOS pipeline triage workflow."""

import argparse
import datetime
import json
import os
from pathlib import Path


def format_entry(entry_id, category, feedback, context, step, note=None):
    """Formats the feedback entry as a dictionary."""
    current_date = datetime.datetime.now().strftime("%d-%B-%Y")
    timestamp = datetime.datetime.now().isoformat()

    entry = {
        "id": entry_id,
        "category": category,
        "date": current_date,
        "timestamp": timestamp,
        "step": step,
        "feedback": feedback,
        "context": context,
        "user": os.environ.get("USER", "unknown"),
        "source": "pipeline-feedback-capture",
    }

    # Add optional note if provided
    if note:
        entry["note"] = note

    return entry


def main():
    parser = argparse.ArgumentParser(description="Save pipeline feedback to a file.")
    parser.add_argument("--category", required=True, help="Category of the feedback")
    parser.add_argument("--feedback", required=True, help="The user's feedback")
    parser.add_argument("--context", required=True, help="Summary of what happened")
    parser.add_argument("--step", required=True, help="The pipeline step being evaluated")
    parser.add_argument("--note", required=False, help="Optional additional note or comment")

    args = parser.parse_args()

    session_id = os.environ.get("CLAUDE_SESSION_ID", f"manual_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}")
    print(f"Session ID: {session_id}")

    # Feedback file in the scripts directory
    script_dir = Path(__file__).parent
    feedback_json_filepath = script_dir / "feedback.json"

    # Create feedback entry as dictionary
    formatted_entry = format_entry(
        session_id,
        args.category,
        args.feedback,
        args.context,
        args.step,
        args.note,
    )

    # Load existing feedback entries or create new list
    feedback_entries = []
    if feedback_json_filepath.exists():
        try:
            with open(feedback_json_filepath) as f:
                feedback_entries = json.load(f)
                if not isinstance(feedback_entries, list):
                    feedback_entries = []
        except Exception as e:
            print(f"Warning: Could not read existing feedback.json: {e}")
            feedback_entries = []

    # Append new entry
    feedback_entries.append(formatted_entry)

    # Save updated feedback.json
    try:
        with open(feedback_json_filepath, "w") as f:
            json.dump(feedback_entries, f, indent=2)
        print(f"\n✓ Successfully saved feedback to {feedback_json_filepath}")
        print(f"  Step: {args.step}")
        print(f"  Category: {args.category}")
        print(f"  Feedback: {args.feedback[:100]}{'...' if len(args.feedback) > 100 else ''}")
        if args.note:
            print(f"  Note: {args.note[:100]}{'...' if len(args.note) > 100 else ''}")
    except Exception as e:
        print(f"✗ Error writing to file: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
