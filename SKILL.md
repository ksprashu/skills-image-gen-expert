---
name: image-gen-expert
description: Advanced image generation and verification using Gemini 3 Pro (Nano Banana Pro) and Flash. Supports character consistency via multimodal reference images and automated quality/compliance verification. Use this skill when the user asks to generate, iterate on, or verify images.
---

# Image Generation Expert

This skill provides specialized tools and workflows for high-fidelity image generation, ensuring character consistency and visual compliance through automated verification.

## Capabilities

1.  **High-Fidelity Generation**: Uses `gemini-3-pro-image-preview` for state-of-the-art image synthesis.
2.  **Character Consistency**: Supports multimodal reference images to maintain identity (e.g., specific characters, logos, or styles) across multiple generations.
3.  **Built-in Assets**: Includes character reference images in `assets/` for quick access (e.g., `char-unit9.png`, `char-pixie.png`, `char-artist.png`, `char-eraser.png`, `char-reboot.png`).
4.  **Automated Verification**: Uses `gemini-3-flash-preview` to programmatically verify that the generated output matches the user's prompt and quality constraints.
5.  **Custom Aspect Ratios**: Supports explicit aspect ratio configuration (e.g., 16:9, 1:1, 4:3).

## Prerequisites

*   **API Key**: Ensure `GOOGLE_API_KEY` is set in the environment. This key must have access to the `gemini-3-pro-image-preview` and `gemini-3-flash-preview` models.
*   **Dependencies**: The bundled script requires `google-genai` and `Pillow` (PIL).

## Usage

### Generating an Image

To generate an image, use the `scripts/image_gen.py` script.

**Basic Usage:**
```bash
python scripts/image_gen.py --prompt "A futuristic cityscape at sunset" --output "city.png"
```

**With Reference Images (Character Consistency):**
```bash
python scripts/image_gen.py --prompt "Unit 9 (Cyberpunk Cat) drinking coffee" --references "path/to/char-unit9.png" --output "unit9_coffee.png"
```

**Custom Aspect Ratio & No Verification:**
```bash
python scripts/image_gen.py --prompt "Cinematic wide shot of a desert" --ar "16:9" --no-verify --output "desert.png"
```

### Script Arguments

| Argument | Description | Default |
| :--- | :--- | :--- |
| `--prompt` | **Required.** The text description of the image. | N/A |
| `--references` | Comma-separated paths to reference images for multimodal input. | None |
| `--ar` | Aspect ratio (e.g., `16:9`, `1:1`, `4:3`). | `1:1` |
| `--output` | Filename for the generated image. | `output.png` |
| `--no-verify` | Skip the automated verification step. | False |
| `--api-key` | Optional override for the `GOOGLE_API_KEY` environment variable. | None |
| `--model` | Image generation model. | `gemini-3-pro-image-preview` |
| `--verifier-model` | Model used for automated verification. | `gemini-3-flash-preview` |

## Workflow Patterns

1.  **Initial Generation**: Start with a clear prompt and let the skill verify the quality.
2.  **Iterative Refinement**: If verification fails or the user wants a change, use the previous output (if applicable) or better reference images to guide the model.
3.  **Verification Failures**: If the script reports a verification failure, analyze the reason provided in the output. This usually indicates that the prompt needs more detail or the model misinterpreted a constraint.

## Troubleshooting

*   **429 Resource Exhausted**: Image generation models often have lower rate limits. The script includes a basic retry, but you may need to wait between calls.
*   **Safety Filters**: If no image is returned, it may have been blocked by safety filters. Try a less sensitive prompt.
*   **Illegible Text**: While Nano Banana is good at text, for complex signs, ensure the prompt explicitly says "reads 'TEXT'". If it fails verification, try again or increase the importance of the text in the prompt.

---

## 🤖 Agent Instructions (Internal)

*As an AI Agent utilizing this skill, follow these operational guidelines:*

### 1. Identify Character Reference Assets
When a user asks to generate a known character (e.g., "Unit 9", "Pixie"), check the `assets/` directory first. Always prefer using the reference image via `--references` to maintain identity consistency.

### 2. Multi-Step Execution Loop
The core script `scripts/image_gen.py` handles verification internally.
- **Observe Output:** Pay attention to the stdout. It will explicitly state `🧐 Verifying image...` followed by `✅ Success` or `🔄 Verification failed: [REASON]`.
- **Failures:** If the script exits with status 1 after failing verification, analyze the reason. If the reason suggests the prompt was misinterpreted, refine the `--prompt` in your next attempt.

### 3. Aspect Ratio Selection
If the user specifies a layout (e.g., "wide", "landscape", "square", "portrait"), map it to the `--ar` argument:
- Landscape/Wide -> `16:9`
- Square -> `1:1`
- Portrait/Tall -> `4:3` (or `9:16` if supported by the model, but the script defaults to standard ratios).

### 4. Handling Timeouts and Rate Limits
Image generation is slow. If you encounter a `429` error, wait at least 10 seconds before retrying. Do not retry more than twice for the same prompt; if it still fails, ask the user for a simpler prompt.

### 5. Verification vs. Speed
By default, always keep verification enabled. Only use `--no-verify` if the user explicitly requests "fast" or "raw" generation, or if the verifier model is consistently hallucinating failures.
