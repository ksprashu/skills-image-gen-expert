# Implementation Plan

## 1. Concept Objective
**Status:** DRAFT
Refactor the `image-gen-expert` skill to transition from a narrow, pre-existing character-focused tool to a dynamic, general-purpose asset generator optimized for blogs, articles, and infographics. The skill must be able to determine what assets are needed and generate them from scratch.

## 2. Problem Breakdown
- **Functional Limitations:** The current documentation (`SKILL.md`, `README.md`) strongly biases the agent toward using specific pre-existing assets (e.g., `char-unit9.png`). This creates tunnel vision for the agent, making it less effective for generic blog posts that require custom infographics, diagrams, or thematic hero images.
- **Technical Architecture:** The underlying Python script (`scripts/image_gen.py`) is actually quite flexible and agnostic. The limitation is primarily in the **Agent Instructions** (`SKILL.md`) and project framing.
- **Asset Management:** The `assets/` folder contains legacy files that reinforce the old paradigm.

## 3. Design Discussion
- **Trade-offs:** Removing the character consistency examples might make it harder for the agent to know *how* to use the `--references` flag.
- **Solution/First Principles:** We should redefine the `--references` flag's use case in the documentation. Instead of "Character Consistency", we frame it as "Brand/Style Consistency" (e.g., providing a brand color palette or style guide image). 
- **Workflow Shift:** The agent needs new instructions on **Asset Determination**. Before generating, it should analyze the provided blog text and identify visual opportunities (e.g., "This section explains a process; let's generate a flowchart/infographic", or "This is the introduction; let's generate a 16:9 hero image").

## 4. Proposed Solution
1. **Redefine Agent Workflows (`SKILL.md`):** Rewrite the internal agent instructions. Introduce a workflow step for "Asset Needs Analysis" based on blog content. Add specific prompting techniques for infographics, diagrams, and thematic illustrations.
2. **Update External Documentation (`README.md`):** Broaden the description to focus on generic content creation, blog asset generation, and style-consistent generation from scratch.
3. **Asset Cleanup:** Remove the narrow `char-*.png` assets from the repository to prevent the agent from anchoring on them, or replace them with a generic `brand-style-guide.png` example.

## 5. Alternatives Considered
- *Alternative 1: Add a new `blog-asset-expert` skill.* Rejected. It's better to make `image-gen-expert` more capable and less constrained rather than duplicating the underlying Python script into a new skill.
- *Alternative 2: Modify `scripts/image_gen.py` to add layout templates.* Rejected. Nano Banana Pro is highly capable of generating infographics purely through prompt engineering; hardcoding layouts in Python limits creativity.

## 6. Revision History
- [2026-04-05] Initial Draft created.

## 7. Implementation Roadmap
- [x] **Task 1: Overhaul `SKILL.md`** - Rewrite capabilities and agent instructions to focus on "Dynamic Blog Asset Generation", "Infographics", and "Style Consistency" over character consistency.
- [x] **Task 2: Clean up `assets/` directory** - Delete legacy `char-*.png` files and optionally add a generic `style-reference.png` to demonstrate brand consistency without locking into specific characters.
- [x] **Task 3: Update `README.md`** - Align the public-facing documentation with the new dynamic, from-scratch asset generation paradigm.

## 8. Review
Plan established. Awaiting user feedback or execution approval.
