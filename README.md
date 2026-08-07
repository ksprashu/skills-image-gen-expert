> [!IMPORTANT]
> **DISCLAIMER & LIABILITY NOTICE**: This is a **personal, individual project** created and maintained entirely by the author (Prashanth). It is **not** an official Google product, it is **not** affiliated with or supported by Google Cloud or Google LLC, and it does **not** come with any official support or warranty. By using this software, you acknowledge that you are solely liable for its use.

# 🎨 Image Gen Expert

[![npx skills](https://img.shields.io/badge/skills.sh-installed-brightgreen)](https://skills.sh)

![Image Gen Expert Header](./docs/images/header.png)

An advanced, high-fidelity custom skill and script pipeline for autonomous visual asset, diagram, and infographic generation inside your agent workspace.

The **Image Gen Expert** uses Google's state-of-the-art **Gemini 3.1 Flash Image** (Nano Banana 2) for versatile 4K image synthesis with an intelligent fallback chain (`gemini-3.1-flash-image` -> `gemini-3.1-flash-lite-image` -> `gemini-3-pro-image`), alongside Gemini vision for multi-step quality and compliance verification.

---

## 🎨 Automatic Series Grounding & Image Editing

The skill automatically leverages reference images (`--references`) across two key workflows:

1. **Automatic Series Visual Cohesion**: When generating a series of graphics for an article or blog (e.g. Hero banner, Flowchart, Infographic), the agent automatically uses the first generated graphic as a style reference for all subsequent graphics.
2. **Image Editing & Iteration**: When editing an existing graphic (e.g., *"Add a Redis caching node to `arch.png`"*), the skill automatically passes `arch.png` as a reference image to preserve the existing visual layout while applying modifications.

---

## 🔄 Generate-Verify-Retry Loop

The skill executes an autonomous verification loop (retrying up to 3 times by default) to ensure that all generated graphics (especially those containing text labels) are legible, correct, and professional before saving:

```mermaid
graph TD
    Start[Draft Blog / Topic Input] --> Analyze[1. Analyze Asset Needs: Hero, Flowchart, Infographic]
    Analyze --> BuildPrompt[2. Build Prompt with Auto-References]
    BuildPrompt --> Synthesis[3. Gemini 3.1 Synthesis & Model Fallback]
    Synthesis --> Verify[4. Gemini Vision Quality Verification]
    Verify -- Pass --> Save[5. Save Asset to disk]
    Verify -- Fail (Attempts < 3) --> Retry[6. Refine Prompt via Gemini based on feedback]
    Retry --> Synthesis
    
    classDef steps fill:#0e101f,stroke:#7c4dff,stroke-width:2px,color:#fff;
    class Start,Analyze,BuildPrompt,Synthesis,Verify,Save,Retry steps;
```

---

## 📂 Repository Structure

The package contents are fully organized for installation via `npx skills`:

| Path | Type | Purpose |
| :--- | :--- | :--- |
| `skills/image-gen-expert/SKILL.md` | Core Instructions | Detailed prompt patterns, aspect ratio mapping rules, and auto-reference guidelines. |
| `skills/image-gen-expert/scripts/image_gen.py` | Python Engine | Executable script that interfaces with Google GenAI API with model fallback chain. |
| `skills/image-gen-expert/assets/` | Style Guides | Optional location to store brand style guidelines and reference pictures. |
| `requirements.txt` | Python Requirements | Defines python libraries required (`google-genai`, `Pillow`). |

---

## 🛠️ Installation & Usage

Install this skill into your agent environment using `npx skills`:

```bash
npx skills add ksprashu/skills-image-gen-expert
```

### Setup Requirements
1. **API Key**: Ensure `GOOGLE_API_KEY` is exported in your environment. If not found, the agent will securely prompt you for it during your interactive session.
2. **Python Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

### Execution Examples

**1. Standalone Hero Banner:**
```bash
python scripts/image_gen.py --prompt "A cinematic hero image representing microservices" --ar "16:9" --output "hero.png"
```

**2. Auto-Grounded Series Diagram (Reusing Hero Style):**
```bash
python scripts/image_gen.py --prompt "An architecture diagram for microservices" --references "hero.png" --ar "4:3" --output "arch.png"
```

**3. Editing an Existing Image:**
```bash
python scripts/image_gen.py --prompt "Based on the reference, add a Redis cache box" --references "arch.png" --ar "4:3" --output "arch_v2.png"
```
