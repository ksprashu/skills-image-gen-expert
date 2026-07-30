# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import time
import io
import pathlib
import argparse
from typing import Optional, List
from google import genai
from PIL import Image

def get_client(api_key: Optional[str] = None):
    key = api_key or os.environ.get("GOOGLE_API_KEY")
    if not key:
        print("❌ Error: GOOGLE_API_KEY not found in environment.")
        print("Please set the GOOGLE_API_KEY environment variable or provide it via the --api-key argument.")
        sys.exit(1)
    return genai.Client(api_key=key)

def refine_prompt(client: genai.Client, original_prompt: str, failure_reason: str, model: str) -> str:
    """Uses Gemini to refine the prompt based on verification feedback."""
    try:
        refinement_prompt = f"""
        You are an expert prompt engineer. We are trying to generate an image using a text-to-image generator.
        The original prompt was: "{original_prompt}"
        The generated image failed verification with the following feedback: "{failure_reason}"
        
        Please rewrite the prompt to address this feedback. Keep the core intent and style, but make specific adjustments, clearer layouts, or stronger guidance on text placement/legibility to resolve the feedback.
        Return ONLY the new refined prompt text. Do not wrap it in extra quotes or markdown blocks.
        """
        response = client.models.generate_content(
            model=model,
            contents=refinement_prompt
        )
        refined = response.text.strip()
        return refined if refined else original_prompt
    except Exception as e:
        print(f"⚠️ Failed to refine prompt automatically: {e}")
        return original_prompt

def verify_image(client: genai.Client, image: Image.Image, prompt: str, model: str) -> tuple[bool, str]:
    """Verify image compliance using Gemini 3 Flash."""
    try:
        verification_prompt = f"""
        Analyze this image against the user's request: "{prompt}".
        
        Strict Constraints:
        1. Subject Accuracy: Does the image accurately represent the core subjects in the prompt?
        2. Text Legibility: If specific text was requested in quotes ('...'), is it present and readable?
        3. Quality: Is the image of high quality and free of obvious artifacts?
        
        Return ONLY 'YES' if it passes, or 'NO: <reason>' if it fails.
        """
        response = client.models.generate_content(
            model=model,
            contents=[verification_prompt, image]
        )
        result = response.text.strip()
        return result.startswith("YES"), result
    except Exception as e:
        print(f"⚠️ Verification API error: {e}")
        return False, f"Verification failed due to API error: {e}"

def main():
    parser = argparse.ArgumentParser(description="Advanced Image Generation with Verification")
    parser.add_argument("--prompt", type=str, required=True, help="Image generation prompt")
    parser.add_argument("--references", type=str, help="Comma-separated paths to reference images")
    parser.add_argument("--ar", type=str, default="1:1", choices=["1:1", "16:9", "4:3", "3:2", "2:3", "3:4", "9:16"], help="Aspect ratio")
    parser.add_argument("--output", type=str, default="output.png", help="Output filename")
    parser.add_argument("--no-verify", action="store_true", help="Disable verification")
    parser.add_argument("--api-key", type=str, help="Override GOOGLE_API_KEY")
    parser.add_argument("--model", type=str, default="gemini-3-pro-image-preview", help="Generation model")
    parser.add_argument("--verifier-model", type=str, default="gemini-3-flash-preview", help="Verifier model")
    
    args = parser.parse_args()
    
    client = get_client(args.api_key)
    
    # Create parent directories for output if they don't exist
    output_path = pathlib.Path(args.output)
    if output_path.parent != pathlib.Path('.'):
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
    # Prepare contents for multimodal request
    current_prompt = args.prompt
    reference_images = []
    
    if args.references:
        for ref_path in args.references.split(","):
            ref_path = ref_path.strip()
            if os.path.exists(ref_path):
                try:
                    reference_images.append(Image.open(ref_path))
                    print(f"📎 Attached reference: {ref_path}")
                except Exception as e:
                    print(f"⚠️ Failed to load reference {ref_path}: {e}")
            else:
                print(f"⚠️ Reference path not found: {ref_path}")

    print(f"🎨 Generating image with model {args.model}...")
    
    max_attempts = 2 if not args.no_verify else 1
    attempt = 0
    
    while attempt < max_attempts:
        try:
            # Build contents list dynamically (since current_prompt can be refined)
            contents = [f"{current_prompt} Aspect Ratio {args.ar}."]
            if reference_images:
                contents.extend(reference_images)
                
            response = client.models.generate_content(
                model=args.model,
                contents=contents
            )
            
            img_data = None
            # Extract image from response parts
            for part in getattr(response, 'parts', []):
                if hasattr(part, 'inline_data') and part.inline_data:
                    img_data = part.inline_data.data
                    break
            
            if not img_data and hasattr(response, 'candidates') and response.candidates:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'inline_data') and part.inline_data:
                        img_data = part.inline_data.data
                        break
            
            if img_data:
                img = Image.open(io.BytesIO(img_data))
                
                if not args.no_verify:
                    print("🧐 Verifying image...")
                    success, reason = verify_image(client, img, current_prompt, args.verifier_model)
                    if success:
                        img.save(args.output)
                        print(f"✅ Success: Image saved to {args.output}")
                        sys.exit(0)
                    else:
                        print(f"🔄 Verification failed: {reason}")
                        attempt += 1
                        if attempt < max_attempts:
                            print("🧐 Refining prompt based on feedback...")
                            current_prompt = refine_prompt(client, current_prompt, reason, args.verifier_model)
                            print(f"📝 New Prompt: {current_prompt}")
                            print("Retrying generation with refined prompt...")
                            continue
                        else:
                            img.save(args.output)
                            print(f"⚠️ Saving unverified image to {args.output} (Max attempts reached)")
                            sys.exit(0)
                else:
                    img.save(args.output)
                    print(f"✅ Success: Image saved to {args.output}")
                    sys.exit(0)
            else:
                print("❌ Error: No image data returned from model.")
                attempt += 1
                
        except Exception as e:
            err_msg = str(e)
            print(f"❌ Error during generation: {e}")
            attempt += 1
            if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg.upper():
                import random
                backoff = (2 ** attempt) * 3 + random.uniform(0.5, 2.0)
                print(f"⏳ Rate limit encountered (429/ResourceExhausted). Retrying with exponential backoff in {backoff:.1f}s...")
                time.sleep(backoff)
            else:
                time.sleep(2)

    sys.exit(1)

if __name__ == "__main__":
    main()
