---
name: image-gen-expert
description: Advanced dynamic image, infographic, and blog asset generation using Gemini 3 Pro (Nano Banana Pro) and Flash. Supports style/brand consistency via multimodal reference images and automated quality/compliance verification. Use this skill when the user asks to generate visual assets for blogs, articles, or diagrams from scratch.
---

# Blog & Content Image Generation Expert

This skill provides specialized tools and workflows for generating high-fidelity, dynamic visual assets for content creation (blogs, articles, documentation), ensuring brand/style consistency and visual compliance through automated verification.

## Capabilities

1.  **Dynamic Asset Needs Analysis**: Capable of reading text (e.g., a blog draft) and determining the most appropriate visual assets (e.g., a flowchart for a process, a 16:9 hero image for the header, an infographic for statistics).
2.  **High-Fidelity Generation**: Uses `gemini-3-pro-image-preview` for state-of-the-art image, diagram, and infographic synthesis.
3.  **Brand & Style Consistency**: Supports multimodal reference images (`--references`) to maintain a specific visual style, color palette, or branding across multiple generations from scratch.
4.  **Automated Verification**: Uses `gemini-3-flash-preview` to programmatically verify that the generated output matches the user's prompt, data accuracy, and quality constraints.
5.  **Custom Aspect Ratios**: Supports explicit aspect ratio configuration (e.g., `16:9` for heroes, `1:1` for inline diagrams, `4:3`).

## Prerequisites

*   **API Key**: Ensure `GOOGLE_API_KEY` is set in the environment. This key must have access to the `gemini-3-pro-image-preview` and `gemini-3-flash-preview` models.
*   **Dependencies**: The bundled script requires `google-genai` and `Pillow` (PIL).

## Usage

### Generating an Asset

To generate an image, use the `scripts/image_gen.py` script.

**Basic Usage (Hero Image):**
```bash
python scripts/image_gen.py --prompt "A cinematic, wide-shot hero image representing modern cloud architecture, corporate blue tones" --ar "16:9" --output "hero.png"
```

**With Reference Images (Style/Brand Consistency):**
```bash
python scripts/image_gen.py --prompt "An infographic explaining the CI/CD pipeline" --references "path/to/brand-style-guide.png" --ar "4:3" --output "cicd_infographic.png"
```

**Custom Aspect Ratio & No Verification (Fast Draft):**
```bash
python scripts/image_gen.py --prompt "A minimalist vector icon of a lightbulb" --ar "1:1" --no-verify --output "icon.png"
```

### Script Arguments

| Argument | Description | Default |
| :--- | :--- | :--- |
| `--prompt` | **Required.** The text description of the image/infographic. | N/A |
| `--references` | Comma-separated paths to reference images for style/brand guidance. | None |
| `--ar` | Aspect ratio (e.g., `16:9`, `1:1`, `4:3`). | `1:1` |
| `--output` | Filename for the generated image. | `output.png` |
| `--no-verify` | Skip the automated verification step. | False |
| `--api-key` | Optional override for the `GOOGLE_API_KEY` environment variable. | None |
| `--model` | Image generation model. | `gemini-3-pro-image-preview` |
| `--verifier-model` | Model used for automated verification. | `gemini-3-flash-preview` |

## Workflow Patterns

1.  **Content Analysis**: Before generating, analyze the source text to determine *what* assets would add value (Hero, Inline Graphic, Diagram, Callout).
2.  **Initial Generation**: Craft a highly specific prompt (including layout and style keywords) and let the skill verify the quality.
3.  **Iterative Refinement**: If verification fails (especially for text legibility in infographics), use the failure reason to refine the prompt, ensuring text is clearly quoted (`reads "TEXT"`).

## Troubleshooting

*   **429 Resource Exhausted**: Image generation models often have lower rate limits. Wait at least 10 seconds between calls.
*   **Safety Filters**: If no image is returned, try a less sensitive prompt.
*   **Illegible Text**: For complex diagrams, ensure the prompt explicitly says "reads 'TEXT'". If it fails verification, try again or simplify the text content.

---

## 🤖 Agent Instructions (Internal)

*As an AI Agent utilizing this skill, follow these operational guidelines:*

### 1. Asset Needs Analysis (Pre-Generation)
When given a blog post or article, do not randomly generate images. First, identify key concepts:
- **Header/Intro**: Suggest a `16:9` Hero Image.
- **Processes/Workflows**: Suggest a Flowchart or Architecture Diagram (`1:1` or `4:3`).
- **Data/Statistics**: Suggest an Infographic.
Formulate a plan for the assets needed from scratch based on the content's tone and subject.

### 2. Brand & Style Consistency
Always prioritize generating assets from scratch over relying on pre-existing content. Use the `--references` flag to pass in generic brand guidelines, color palettes, or mood boards if requested, ensuring all assets generated for a single blog match stylistically.

### 3. Multi-Step Execution Loop
The core script `scripts/image_gen.py` handles verification internally.
- **Observe Output:** Pay attention to the stdout (`🧐 Verifying image...`).
- **Failures:** If verification fails, it's often due to text in infographics. Adjust your `--prompt` to be simpler or more explicit about text placement, then retry.

### 4. Aspect Ratio Mapping
Map the required asset type to the optimal `--ar` argument:
- **Hero / Header**: `16:9`
- **Standard Inline / Diagram**: `4:3`
- **Icon / Spot Illustration**: `1:1`

### 5. Prompt Engineering for Content Assets
- **Infographics**: Use keywords like *"flat vector illustration, clean lines, infographic layout, solid background"*.
- **Diagrams**: Use keywords like *"flowchart, nodes and edges, technical diagram, clear text labels"*.
- **Photographic Heroes**: Use keywords like *"cinematic lighting, photorealistic, wide shot, negative space for text"*.
