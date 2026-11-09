import random

import pytest

from wingdash import constants as c
from wingdash import logic

GROUND_Y = c.SCREEN_HEIGHT * c.GROUND_RATIO
PIPE_W, PIPE_H, PLAYER_H = 52, 320, 24


def test_gravity_accelerates_until_max_velocity():
    assert logic.apply_gravity(0, flapped=False) == c.GRAVITY
    assert logic.apply_gravity(c.MAX_VELOCITY, flapped=False) == c.MAX_VELOCITY


def test_gravity_is_skipped_on_flap_frame():
    assert logic.apply_gravity(c.FLAP_VELOCITY, flapped=True) == c.FLAP_VELOCITY


def test_bird_stops_at_ground():
    y = logic.advance_y(380, 10, GROUND_Y, PLAYER_H)
    assert y == pytest.approx(GROUND_Y - PLAYER_H)


def test_bird_moves_freely_in_open_air():
    assert logic.advance_y(100, 5, GROUND_Y, PLAYER_H) == 105


def test_bounds_collision():
    assert logic.hits_bounds(-1, GROUND_Y)
    assert logic.hits_bounds(GROUND_Y - c.GROUND_HIT_MARGIN + 1, GROUND_Y)
    assert not logic.hits_bounds(100, GROUND_Y)
    assert not logic.hits_bounds(0, GROUND_Y)


def test_pipe_collision_upper_and_lower():
    upper = [{"x": 100, "y": -200}]  # bottom edge at y=120
    lower = [{"x": 100, "y": 220}]
    assert logic.hits_pipe(100, 50, PLAYER_H, upper, lower, PIPE_W, PIPE_H)
    assert logic.hits_pipe(100, 210, PLAYER_H, upper, lower, PIPE_W, PIPE_H)


def test_bird_passes_through_gap_and_far_pipes():
    upper = [{"x": 100, "y": -200}]
    lower = [{"x": 100, "y": 220}]
    assert not logic.hits_pipe(100, 150, PLAYER_H, upper, lower, PIPE_W, PIPE_H)
    assert not logic.hits_pipe(300, 50, PLAYER_H, upper, lower, PIPE_W, PIPE_H)


def test_score_triggers_only_on_the_crossing_frame():
    pipe_x = 24  # pipe centre at x=50 for a 52px pipe
    assert logic.crossed_pipe(50, pipe_x, PIPE_W)
    assert logic.crossed_pipe(53, pipe_x, PIPE_W)
    assert not logic.crossed_pipe(54, pipe_x, PIPE_W)
    assert not logic.crossed_pipe(49, pipe_x, PIPE_W)


@pytest.mark.parametrize("seed", range(20))
def test_random_pipe_pair_keeps_fixed_gap(seed):
    upper, lower = logic.random_pipe_pair(
        300, c.SCREEN_HEIGHT, base_height=112, pipe_height=PIPE_H, rng=random.Random(seed)
    )
    gap = lower["y"] - (upper["y"] + PIPE_H)
    assert gap == pytest.approx(c.SCREEN_HEIGHT * c.PIPE_GAP_RATIO)
    assert upper["x"] == lower["x"] == 300


def test_gravity_never_exceeds_max_velocity_over_many_frames():
    velocity = c.FLAP_VELOCITY
    for _ in range(100):
        velocity = logic.apply_gravity(velocity, flapped=False)
    assert velocity == c.MAX_VELOCITY


def test_upward_velocity_moves_the_bird_up():
    assert logic.advance_y(200, -8, GROUND_Y, PLAYER_H) == 192


def test_pipe_touching_horizontally_exactly_is_not_a_hit():
    upper = [{"x": 100 + PIPE_W, "y": -200}]
    assert not logic.hits_pipe(100, 50, PLAYER_H, upper, [], PIPE_W, PIPE_H)


def test_collision_combines_bounds_and_pipes():
    upper = [{"x": 100, "y": -200}]
    lower = [{"x": 100, "y": 220}]
    args = (upper, lower, PIPE_W, PIPE_H, GROUND_Y)
    assert logic.is_collision(100, 50, PLAYER_H, *args)  # inside the upper pipe
    assert logic.is_collision(500, -5, PLAYER_H, *args)  # left through the top
    assert not logic.is_collision(500, 100, PLAYER_H, *args)  # open air, no pipe nearby


@pytest.mark.parametrize("seed", range(20))
def test_random_pipe_pair_stays_on_screen_above_the_base(seed):
    base_h = 112
    upper, lower = logic.random_pipe_pair(
        300, c.SCREEN_HEIGHT, base_height=base_h, pipe_height=PIPE_H, rng=random.Random(seed)
    )
    assert lower["y"] > 0
    assert lower["y"] < c.SCREEN_HEIGHT - base_h
    assert upper["y"] < 0


def test_random_pipe_pair_is_reproducible_with_a_seed():
    first = logic.random_pipe_pair(300, c.SCREEN_HEIGHT, 112, PIPE_H, rng=random.Random(7))
    second = logic.random_pipe_pair(300, c.SCREEN_HEIGHT, 112, PIPE_H, rng=random.Random(7))
    assert first == second


def test_a_bird_that_never_flaps_eventually_hits_the_ground():
    y, velocity = float(c.PLAYER_START_Y), 0
    for _ in range(200):
        velocity = logic.apply_gravity(velocity, flapped=False)
        y = logic.advance_y(y, velocity, GROUND_Y, PLAYER_H)
    assert logic.hits_bounds(y, GROUND_Y)
