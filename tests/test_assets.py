"""Checks that every asset the game loads is present, and that loading works without a display."""

import os

import pytest

from wingdash import assets

SPRITES = [f"{d}.png" for d in range(10)] + ["message.png", "base.png", "background.png", "bird.png", "pipe.png"]
SOUNDS = ["wing", "hit", "point"]


@pytest.mark.parametrize("name", SPRITES)
def test_sprite_files_ship_with_the_package(name):
    assert (assets.SPRITES_DIR / name).is_file()


@pytest.mark.parametrize("name", SOUNDS)
def test_required_sounds_ship_with_the_package(name):
    assert (assets.SOUNDS_DIR / f"{name}.wav").is_file()


def test_assets_load_with_dummy_video_and_audio():
    pygame = pytest.importorskip("pygame")
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
    pygame.init()
    try:
        pygame.display.set_mode((10, 10))
        sprites = assets.load_sprites()
        assert len(sprites["numbers"]) == 10
        upper, lower = sprites["pipe"]
        assert upper.get_size() == lower.get_size()
        sounds = assets.load_sounds()
        assert set(SOUNDS) <= set(sounds)
    finally:
        pygame.quit()
