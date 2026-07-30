#!/usr/bin/env python3
# Copyright 2026 Google LLC
# Static Verifier for EGA-C05A Skill Deep Review

import sys
import json
import re
from pathlib import Path

def main():
    artifact_path = Path("/Users/ksprashanth/code/github/skills-image-gen-expert/.gemini/harness/EGA-C05A/deliverable.md")
    if not artifact_path.exists():
        print(json.dumps({"status": "FAIL", "errors": [f"Artifact file missing: {artifact_path}"]}, indent=2))
        sys.exit(1)

    content = artifact_path.read_text(encoding="utf-8")
    errors = []

    # Check minimum word count (at least 600 words for a deep review)
    words = len(content.split())
    if words < 500:
        errors.append(f"Content too short ({words} words, minimum is 500)")

    # Check for placeholder terms
    prohibited = ["TBD", "TODO", "as an AI", "FILL_ME_IN"]
    for term in prohibited:
        if re.search(rf"\b{re.escape(term)}\b", content, re.IGNORECASE):
            errors.append(f"Contains prohibited placeholder: '{term}'")

    # Required sections
    required_sections = [
        "Executive Summary",
        "Architecture & Component Analysis",
        "Code Audit",
        "Key Findings",
        "Actionable Recommendations"
    ]
    for section in required_sections:
        if section.lower() not in content.lower():
            errors.append(f"Missing required section: '{section}'")

    if errors:
        print(json.dumps({"status": "FAIL", "errors": errors}, indent=2))
        sys.exit(1)

    print(json.dumps({"status": "PASS"}, indent=2))
    sys.exit(0)

if __name__ == "__main__":
    main()
