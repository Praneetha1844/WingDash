"""Tunable game constants. Pure Python so the game logic can be tested without pygame."""

FPS = 32

SCREEN_WIDTH = 289
SCREEN_HEIGHT = 511
GROUND_RATIO = 0.8  # ground line as a fraction of the screen height
GROUND_HIT_MARGIN = 25  # bird counts as grounded this far above the ground line

MESSAGE_X = -40  # horizontal offset of the title sprite on the welcome screen

PIPE_VELOCITY_X = -4
PIPE_SPAWN_X = SCREEN_WIDTH + 10
FIRST_PIPE_X = SCREEN_WIDTH + 200
PIPE_GAP_RATIO = 1 / 3  # vertical gap between pipes, as a fraction of the screen height
PIPE_SPAWN_WINDOW = 5  # spawn the next pair when the leading pipe is within this many px of x=0

PLAYER_X = SCREEN_WIDTH // 5
PLAYER_START_Y = SCREEN_WIDTH // 2
INITIAL_VELOCITY = -9
MAX_VELOCITY = 10
FLAP_VELOCITY = -8
GRAVITY = 1

SCORE_Y_RATIO = 0.12
