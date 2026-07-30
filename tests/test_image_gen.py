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
        success, reason = image_gen.verify_image(mock_client, mock_image, "A test prompt", "gemini-3-flash-preview")

        self.assertTrue(success)
        self.assertEqual(reason, "YES")

    def test_verify_image_failure_reasons(self):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "NO: Text is unreadable"
        mock_client.models.generate_content.return_value = mock_response

        mock_image = MagicMock()
        success, reason = image_gen.verify_image(mock_client, mock_image, "A test prompt", "gemini-3-flash-preview")

        self.assertFalse(success)
        self.assertEqual(reason, "NO: Text is unreadable")

    def test_verify_image_api_exception_handling(self):
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = Exception("API Quota Exceeded")

        mock_image = MagicMock()
        success, reason = image_gen.verify_image(mock_client, mock_image, "A test prompt", "gemini-3-flash-preview")

        # Must return False on API exception to avoid silent pass
        self.assertFalse(success)
        self.assertIn("Verification failed due to API error", reason)

    def test_refine_prompt_success(self):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Refined prompt with readable text 'CLOUD'"
        mock_client.models.generate_content.return_value = mock_response

        refined = image_gen.refine_prompt(mock_client, "Original prompt", "Text unreadable", "gemini-3-flash-preview")
        self.assertEqual(refined, "Refined prompt with readable text 'CLOUD'")

    def test_refine_prompt_exception_fallback(self):
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = Exception("API error")

        refined = image_gen.refine_prompt(mock_client, "Original prompt", "Text unreadable", "gemini-3-flash-preview")
        # Should fallback gracefully to original prompt
        self.assertEqual(refined, "Original prompt")

if __name__ == "__main__":
    unittest.main()
