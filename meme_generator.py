"""Create simple memes locally so the bot does not depend on a third-party API."""

from __future__ import annotations

from io import BytesIO
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont

MAX_PROMPT_LENGTH = 500
IMAGE_SIZE = (1200, 675)


def validate_prompt(prompt: str) -> str:
    """Return a normalized prompt or raise ValueError for invalid input."""
    normalized = " ".join(prompt.split())
    if not normalized:
        raise ValueError("Please provide a prompt for the meme.")
    if len(normalized) > MAX_PROMPT_LENGTH:
        raise ValueError(f"Prompts must be {MAX_PROMPT_LENGTH} characters or fewer.")
    return normalized


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", size)
    except OSError:
        return ImageFont.load_default()


def generate_meme(prompt: str) -> BytesIO:
    """Render a prompt as a shareable PNG meme."""
    prompt = validate_prompt(prompt)
    image = Image.new("RGB", IMAGE_SIZE, (28, 31, 40))
    draw = ImageDraw.Draw(image)

    # A subtle diagonal pattern keeps the generated image readable but less plain.
    for x in range(-IMAGE_SIZE[1], IMAGE_SIZE[0], 80):
        draw.line((x, 0, x + IMAGE_SIZE[1], IMAGE_SIZE[1]), fill=(40, 44, 54), width=3)

    title_font = _font(64)
    body_font = _font(48)
    footer_font = _font(26)
    draw.text((60, 42), "MEME BOT", font=title_font, fill="white", stroke_width=2, stroke_fill="black")

    lines = wrap(prompt, width=34)
    line_height = 62
    total_height = len(lines) * line_height
    y = (IMAGE_SIZE[1] - total_height) // 2
    for line in lines:
        box = draw.textbbox((0, 0), line, font=body_font, stroke_width=2)
        x = (IMAGE_SIZE[0] - (box[2] - box[0])) // 2
        draw.text((x, y), line, font=body_font, fill="white", stroke_width=2, stroke_fill="black")
        y += line_height

    draw.text((60, IMAGE_SIZE[1] - 58), "prompt-powered comedy", font=footer_font, fill=(190, 195, 205))
    output = BytesIO()
    image.save(output, format="PNG", optimize=True)
    output.seek(0)
    return output
