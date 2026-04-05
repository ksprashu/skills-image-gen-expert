# Evidence Ledger

| ID | Topic | Source | Why authoritative | Last-checked |
|---|---|---|---|---|
| E-001 | Repository Structure | `ls -R` | Direct file system observation | 2026-04-04 |
| E-002 | Dependencies | `requirements.txt` | Official dependency manifest | 2026-04-04 |
| E-003 | Core Logic | `scripts/image_gen.py` | Implementation source code | 2026-04-04 |
| E-004 | Project Vision | `README.md` | Official project documentation | 2026-04-04 |
| E-008 | Repository URL | `git remote -v` | Direct command output from git | 2026-04-04 |
| E-009 | Link Verification | `grep "YOUR_ORG" README.md CONTRIBUTING.md` | Search for remaining placeholders. | 2026-04-04 |
| E-013 | API Key Prompting | `SKILL.md`, `README.md` | Documentation of the secure prompting protocol | 2026-04-05 |
| E-014 | Error Messaging | `scripts/image_gen.py` | Implementation of clearer error message for key missing | 2026-04-05 |
| E-015 | Runtime Verification | `.venv/bin/python3 scripts/image_gen.py` | Manual check of the error output | 2026-04-05 |
