"""Loads sprites and sounds that ship inside the package (``wingdash/resources``)."""

from pathlib import Path

import pygame

RESOURCES_DIR = Path(__file__).resolve().parent / "resources"
SPRITES_DIR = RESOURCES_DIR / "sprites"
SOUNDS_DIR = RESOURCES_DIR / "sounds"


def _image(name, alpha=True):
    image = pygame.image.load(str(SPRITES_DIR / name))
    return image.convert_alpha() if alpha else image.convert()


def load_sprites():
    """Load every sprite. Call after the display mode has been set."""
    pipe = _image("pipe.png")
    return {
        "numbers": tuple(_image(f"{digit}.png") for digit in range(10)),
        "message": _image("message.png"),
        "base": _image("base.png"),
        "background": _image("background.png", alpha=False),
        "player": _image("bird.png"),
        "pipe": (pygame.transform.rotate(pipe, 180), pipe),  # (upper, lower)
    }


class _SilentSound:
    """Stand-in used when no audio device is available, so the game still runs."""

    def play(self):
        return None


def load_sounds():
    """Load all wav files, keyed by file name without extension (wing, hit, point, ...).

    Falls back to silent stand-ins if the audio mixer could not start.
    """
    paths = sorted(SOUNDS_DIR.glob("*.wav"))
    if not pygame.mixer.get_init():
        return {path.stem: _SilentSound() for path in paths}
    return {path.stem: pygame.mixer.Sound(str(path)) for path in paths}
