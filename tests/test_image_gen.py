# Copyright 2026 Google LLC
# Unit Tests for image_gen.py CLI and helper functions

import unittest
from unittest.mock import MagicMock, patch
import os
import sys
import pathlib

# Import image_gen module from skills directory
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "skills/image-gen-expert/scripts"))
import image_gen

class TestImageGenHelpers(unittest.TestCase):

    def test_verify_image_success(self):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "YES"
        mock_client.models.generate_content.return_value = mock_response

        mock_image = MagicMock()
        success, reason = image_gen.verify_image(mock_client, mock_image, "A test prompt", "gemini-3.1-flash-image")

        self.assertTrue(success)
        self.assertEqual(reason, "YES")

    def test_verify_image_failure_reasons(self):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "NO: Text is unreadable"
        mock_client.models.generate_content.return_value = mock_response

        mock_image = MagicMock()
        success, reason = image_gen.verify_image(mock_client, mock_image, "A test prompt", "gemini-3.1-flash-image")

        self.assertFalse(success)
        self.assertEqual(reason, "NO: Text is unreadable")

    def test_verify_image_api_exception_handling(self):
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = Exception("API Quota Exceeded")

        mock_image = MagicMock()
        success, reason = image_gen.verify_image(mock_client, mock_image, "A test prompt", "gemini-3.1-flash-image")

        # Must return False on API exception to avoid silent pass
        self.assertFalse(success)
        self.assertIn("Verification failed due to API error", reason)

    def test_refine_prompt_success(self):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Refined prompt with readable text 'CLOUD'"
        mock_client.models.generate_content.return_value = mock_response

        refined = image_gen.refine_prompt(mock_client, "Original prompt", "Text unreadable", "gemini-3.1-flash-image")
        self.assertEqual(refined, "Refined prompt with readable text 'CLOUD'")

    def test_refine_prompt_exception_fallback(self):
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = Exception("API error")

        refined = image_gen.refine_prompt(mock_client, "Original prompt", "Text unreadable", "gemini-3.1-flash-image")
        # Should fallback gracefully to original prompt
        self.assertEqual(refined, "Original prompt")

    def test_get_fallback_chain_without_references(self):
        chain = image_gen.get_fallback_chain("gemini-3.1-flash-image", has_references=False)
        expected = [
            "gemini-3.1-flash-image",
            "gemini-3.1-flash-lite-image",
            "gemini-3-pro-image",
            "gemini-3-pro-image-preview"
        ]
        self.assertEqual(chain, expected)

    def test_get_fallback_chain_with_references_filters_lite(self):
        chain = image_gen.get_fallback_chain("gemini-3.1-flash-image", has_references=True)
        # Should exclude flash-lite because it's not optimized for multi-reference input
        self.assertNotIn("gemini-3.1-flash-lite-image", chain)
        expected = [
            "gemini-3.1-flash-image",
            "gemini-3-pro-image",
            "gemini-3-pro-image-preview"
        ]
        self.assertEqual(chain, expected)

    def test_generate_with_fallback_cascades_on_error(self):
        mock_client = MagicMock()
        # First model fails, second model succeeds
        part_mock = MagicMock()
        part_mock.inline_data.data = b"fake_png_data"
        
        success_response = MagicMock()
        success_response.parts = [part_mock]

        def side_effect(model, contents):
            if model == "gemini-3.1-flash-image":
                raise Exception("429 ResourceExhausted")
            return success_response

        mock_client.models.generate_content.side_effect = side_effect

        chain = ["gemini-3.1-flash-image", "gemini-3.1-flash-lite-image"]
        
        with patch("PIL.Image.open") as mock_open:
            mock_open.return_value = MagicMock()
            img, used_model = image_gen.generate_with_fallback(mock_client, ["test prompt"], chain)
            self.assertIsNotNone(img)
            self.assertEqual(used_model, "gemini-3.1-flash-lite-image")

if __name__ == "__main__":
    unittest.main()
