"""Loads sprites and sounds from the repository's assets directory."""

from pathlib import Path

import pygame

ASSETS_DIR = Path(__file__).resolve().parents[2] / "assets"
SPRITES_DIR = ASSETS_DIR / "sprites"
SOUNDS_DIR = ASSETS_DIR / "sounds"


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


def load_sounds():
    """Load all wav files, keyed by file name without extension (wing, hit, point, ...)."""
    return {path.stem: pygame.mixer.Sound(str(path)) for path in SOUNDS_DIR.glob("*.wav")}
