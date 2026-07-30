#!/usr/bin/env python3
# Copyright 2026 Google LLC
# Static Verifier for EGA-E65D Implementation Pass

import sys
import json
import subprocess
from pathlib import Path

def main():
    errors = []
    base_dir = Path("/Users/ksprashanth/code/github/skills-image-gen-expert")

    # 1. Check scripts/image_gen.py
    script_path = base_dir / "skills/image-gen-expert/scripts/image_gen.py"
    if not script_path.exists():
        errors.append(f"Script missing: {script_path}")
    else:
        content = script_path.read_text(encoding="utf-8")
        # Check that exception in verify_image does not return True
        if "return True, f\"Verification skipped due to error:" in content:
            errors.append("verify_image() still silently returns True on verification exception")
        
        # Check for exponential backoff or 429 rate limit handling
        if "429" not in content and "ResourceExhausted" not in content and "exponential" not in content.lower() and "backoff" not in content.lower():
            errors.append("image_gen.py missing rate-limit / 429 retry backoff logic")

    # 2. Check references/ directory files
    ref_dir = base_dir / "skills/image-gen-expert/references"
    ref_files = list(ref_dir.glob("*.md"))
    if not ref_files:
        errors.append(f"No reference markdown documentation found in {ref_dir}")

    # 3. Check test suite execution
    test_file = base_dir / "tests/test_image_gen.py"
    if not test_file.exists():
        errors.append(f"Test suite missing: {test_file}")
    else:
        res = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests"], cwd=base_dir, capture_output=True, text=True)
        if res.returncode != 0:
            errors.append(f"Unit test suite failed:\n{res.stderr or res.stdout}")

    # 4. Check deliverable artifact
    deliverable = base_dir / ".gemini/harness/EGA-E65D/deliverable.md"
    if not deliverable.exists():
        errors.append(f"Deliverable summary missing: {deliverable}")

    if errors:
        print(json.dumps({"status": "FAIL", "errors": errors}, indent=2))
        sys.exit(1)

    print(json.dumps({"status": "PASS"}, indent=2))
    sys.exit(0)

if __name__ == "__main__":
    main()
