"""Pure game rules: physics, collisions, scoring and pipe generation (no pygame)."""

import random

from wingdash import constants as c


def apply_gravity(velocity, flapped):
    """Return the next vertical velocity. Gravity is skipped on the frame the bird flaps."""
    if velocity < c.MAX_VELOCITY and not flapped:
        return velocity + c.GRAVITY
    return velocity


def advance_y(player_y, velocity, ground_y, player_height):
    """Move the bird, stopping it at the ground."""
    return player_y + min(velocity, ground_y - player_y - player_height)


def hits_bounds(player_y, ground_y):
    """True if the bird touched the ground or left through the top of the screen."""
    return player_y > ground_y - c.GROUND_HIT_MARGIN or player_y < 0


def hits_pipe(player_x, player_y, player_height, upper_pipes, lower_pipes, pipe_width, pipe_height):
    """True if the bird overlaps any upper or lower pipe. Pipes are dicts with x and y."""
    for pipe in upper_pipes:
        if player_y < pipe_height + pipe["y"] and abs(player_x - pipe["x"]) < pipe_width:
            return True
    for pipe in lower_pipes:
        if player_y + player_height > pipe["y"] and abs(player_x - pipe["x"]) < pipe_width:
            return True
    return False


def is_collision(
    player_x, player_y, player_height, upper_pipes, lower_pipes, pipe_width, pipe_height, ground_y
):
    return hits_bounds(player_y, ground_y) or hits_pipe(
        player_x, player_y, player_height, upper_pipes, lower_pipes, pipe_width, pipe_height
    )


def crossed_pipe(player_mid_x, pipe_x, pipe_width):
    """True on the single frame when the bird's centre passes the pipe's centre."""
    pipe_mid = pipe_x + pipe_width / 2
    return pipe_mid <= player_mid_x < pipe_mid + abs(c.PIPE_VELOCITY_X)


def random_pipe_pair(x, screen_height, base_height, pipe_height, rng=random):
    """Return (upper, lower) pipe dicts at x with a fixed gap at a random height."""
    gap = screen_height * c.PIPE_GAP_RATIO
    lower_y = gap + rng.randrange(0, int(screen_height - base_height - 1.2 * gap))
    upper_y = lower_y - gap - pipe_height  # upper pipe is drawn from above the screen
    return {"x": x, "y": upper_y}, {"x": x, "y": lower_y}
