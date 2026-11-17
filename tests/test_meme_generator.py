import unittest
from io import BytesIO

from PIL import Image

from meme_generator import IMAGE_SIZE, MAX_PROMPT_LENGTH, generate_meme, validate_prompt


class MemeGeneratorTests(unittest.TestCase):
    def test_validate_prompt_normalizes_whitespace(self):
        self.assertEqual(validate_prompt("  ship   it\nnow "), "ship it now")

    def test_validate_prompt_rejects_invalid_prompts(self):
        for prompt in ("", "   ", "x" * (MAX_PROMPT_LENGTH + 1)):
            with self.assertRaises(ValueError):
                validate_prompt(prompt)

    def test_generate_meme_returns_png_with_expected_dimensions(self):
        output = generate_meme("when the tests pass")

        self.assertIsInstance(output, BytesIO)
        with Image.open(output) as image:
            self.assertEqual(image.format, "PNG")
            self.assertEqual(image.size, IMAGE_SIZE)
