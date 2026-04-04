# Contributing to Image Generation Expert

Thank you for your interest in contributing to the Image Generation Expert skill! This guide will help you get started with development and outline our standards.

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.9 or higher.
- [Gemini CLI](https://geminicli.com) installed.
- A Google AI Studio or Google Cloud API Key with access to `gemini-3-pro-image-preview` and `gemini-3-flash-preview`.

### 2. Setup
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/ksprashu/skills-image-gen-expert.git
    cd skills-image-gen-expert
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set your API Key:**
    ```bash
    export GOOGLE_API_KEY="your-api-key-here"
    ```

### 3. Local Development & Testing
To test changes to the core generation logic:
```bash
python scripts/image_gen.py --prompt "Test prompt" --output "test_output.png"
```

To test the skill within the Gemini CLI:
1.  Link the skill: `gemini skills link .`
2.  In a session, reload skills: `/skills reload`
3.  Execute a command: `Use the image-gen-expert skill to generate a simple logo.`

## 🛠️ Coding Standards

- **Style:** Follow [PEP 8](https://peps.python.org/pep-0008/) for Python code.
- **Typing:** Use type hints for all function signatures and complex variables.
- **Documentation:** Provide docstrings (Google style preferred) for all public functions and classes.
- **Simplicity:** Prefer readable, deterministic logic over complex abstractions.

## 🤝 Before you begin

### Sign our Contributor License Agreement

Contributions to this project must be accompanied by a
[Contributor License Agreement](https://cla.developers.google.com/about) (CLA).
You (or your employer) retain the copyright to your contribution; this simply
gives us permission to use and redistribute your contributions as part of the
project.

If you or your current employer have already signed the Google CLA (even if it
was for a different project), you probably don't need to do it again.

Visit <https://cla.developers.google.com/> to see your current agreements or to
sign a new one.

### Review our Community Guidelines

This project follows [Google's Open Source Community
Guidelines](https://opensource.google/conduct/).

## 🤝 Pull Request Process

1.  **Create a Branch:** Use a descriptive name (e.g., `feat/add-new-verifier` or `fix/issue-123`).
2.  **Verify Locally:** Ensure your changes pass manual testing and don't introduce regressions.
3.  **Update Documentation:** If you add a new feature or change an existing one, update `README.md` and `SKILL.md` accordingly.
4.  **Submit PR:** Provide a clear description of the change, the problem it solves, and how you verified it.

## ⚖️ License
By contributing, you agree that your contributions will be licensed under the Apache License, Version 2.0.
