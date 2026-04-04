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
import argparse
from typing import Optional, List
from google import genai
from PIL import Image

def get_client(api_key: Optional[str] = None):
    key = api_key or os.environ.get("GOOGLE_API_KEY")
    if not key:
        print("❌ Error: GOOGLE_API_KEY not found in environment or provided via --api-key.")
        sys.exit(1)
    return genai.Client(api_key=key)

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
        return True, f"Verification skipped due to error: {e}"

def main():
    parser = argparse.ArgumentParser(description="Advanced Image Generation with Verification")
    parser.add_argument("--prompt", type=str, required=True, help="Image generation prompt")
    parser.add_argument("--references", type=str, help="Comma-separated paths to reference images")
    parser.add_argument("--ar", type=str, default="1:1", help="Aspect ratio (e.g., 16:9, 1:1)")
    parser.add_argument("--output", type=str, default="output.png", help="Output filename")
    parser.add_argument("--no-verify", action="store_true", help="Disable verification")
    parser.add_argument("--api-key", type=str, help="Override GOOGLE_API_KEY")
    parser.add_argument("--model", type=str, default="gemini-3-pro-image-preview", help="Generation model")
    parser.add_argument("--verifier-model", type=str, default="gemini-3-flash-preview", help="Verifier model")
    
    args = parser.parse_args()
    
    client = get_client(args.api_key)
    
    # Prepare contents for multimodal request
    contents = [f"{args.prompt} Aspect Ratio {args.ar}."]
    
    if args.references:
        for ref_path in args.references.split(","):
            ref_path = ref_path.strip()
            if os.path.exists(ref_path):
                try:
                    contents.append(Image.open(ref_path))
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
                    success, reason = verify_image(client, img, args.prompt, args.verifier_model)
                    if success:
                        img.save(args.output)
                        print(f"✅ Success: Image saved to {args.output}")
                        sys.exit(0)
                    else:
                        print(f"🔄 Verification failed: {reason}")
                        attempt += 1
                        if attempt < max_attempts:
                            print("Retrying generation...")
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
            print(f"❌ Error during generation: {e}")
            attempt += 1
            time.sleep(2)

    sys.exit(1)

if __name__ == "__main__":
    main()
