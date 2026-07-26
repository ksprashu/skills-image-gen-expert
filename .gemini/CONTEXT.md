# Project Context: skills-image-gen-expert

## 1. Vision & Purpose
*   **Goal:** Provide an advanced image generation and verification skill for Google Antigravity and Agentic AI tools.
*   **Core Logic:** Uses `gemini-3-pro-image-preview` for generation and `gemini-3-flash-preview` for quality/compliance verification. Supports character consistency via multimodal reference images.

## 2. Technical Stack
*   **Language:** Python 3.9+
*   **Key Libraries:** `google-genai` (>=0.1.1), `Pillow` (>=10.0.0).
*   **APIs:** Google AI Studio or Google Cloud API (Gemini 3 Pro/Flash).

## 3. Standards & Constraints
*   **Style:** CLI-based Python script (`scripts/image_gen.py`) using `argparse`.
*   **Testing:** Manual script usage via `python scripts/image_gen.py`.
*   **Safety:** Requires `GOOGLE_API_KEY` for model access.
