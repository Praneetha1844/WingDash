"""Pygame front end: welcome screen and the main game loop."""

import sys

import pygame
from pygame.locals import K_ESCAPE, K_SPACE, K_UP, KEYDOWN, QUIT

from wingdash import constants as c
from wingdash import logic
from wingdash.assets import load_sounds, load_sprites


def _quit_requested(event):
    return event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE)


def _flap_requested(event):
    return event.type == KEYDOWN and event.key in (K_SPACE, K_UP)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("WingDash")
        self.screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.sprites = load_sprites()
        self.sounds = load_sounds()
        self.ground_y = c.SCREEN_HEIGHT * c.GROUND_RATIO

    def run(self):
        while True:
            self.welcome()
            self.play()

    @staticmethod
    def _exit():
        pygame.quit()
        sys.exit()

    def welcome(self):
        """Show the title screen until the player flaps."""
        player = self.sprites["player"]
        player_y = (c.SCREEN_HEIGHT - player.get_height()) / 2
        while True:
            for event in pygame.event.get():
                if _quit_requested(event):
                    self._exit()
                if _flap_requested(event):
                    return
            self.screen.blit(self.sprites["background"], (0, 0))
            self.screen.blit(player, (c.PLAYER_X, player_y))
            self.screen.blit(self.sprites["message"], (c.MESSAGE_X, 0))
            self.screen.blit(self.sprites["base"], (0, self.ground_y))
            pygame.display.update()
            self.clock.tick(c.FPS)

    def play(self):
        """Run one round. Returns when the bird crashes."""
        sprites, sounds = self.sprites, self.sounds
        pipe_w = sprites["pipe"][0].get_width()
        pipe_h = sprites["pipe"][0].get_height()
        player_w = sprites["player"].get_width()
        player_h = sprites["player"].get_height()
        base_h = sprites["base"].get_height()

        def new_pair(x):
            return logic.random_pipe_pair(x, c.SCREEN_HEIGHT, base_h, pipe_h)

        first = new_pair(c.FIRST_PIPE_X)
        second = new_pair(c.FIRST_PIPE_X + c.SCREEN_WIDTH / 2)
        upper_pipes = [first[0], second[0]]
        lower_pipes = [first[1], second[1]]

        score = 0
        player_y = c.PLAYER_START_Y
        velocity = c.INITIAL_VELOCITY

        while True:
            flapped = False
            for event in pygame.event.get():
                if _quit_requested(event):
                    self._exit()
                if _flap_requested(event) and player_y > 0:
                    velocity = c.FLAP_VELOCITY
                    flapped = True
                    sounds["wing"].play()

            if logic.is_collision(
                c.PLAYER_X, player_y, player_h, upper_pipes, lower_pipes, pipe_w, pipe_h, self.ground_y
            ):
                sounds["hit"].play()
                return

            player_mid_x = c.PLAYER_X + player_w / 2
            for pipe in upper_pipes:
                if logic.crossed_pipe(player_mid_x, pipe["x"], pipe_w):
                    score += 1
                    sounds["point"].play()

            velocity = logic.apply_gravity(velocity, flapped)
            player_y = logic.advance_y(player_y, velocity, self.ground_y, player_h)

            for upper, lower in zip(upper_pipes, lower_pipes):
                upper["x"] += c.PIPE_VELOCITY_X
                lower["x"] += c.PIPE_VELOCITY_X

            if 0 < upper_pipes[0]["x"] < c.PIPE_SPAWN_WINDOW:
                upper, lower = new_pair(c.PIPE_SPAWN_X)
                upper_pipes.append(upper)
                lower_pipes.append(lower)

            if upper_pipes[0]["x"] < -pipe_w:
                upper_pipes.pop(0)
                lower_pipes.pop(0)

            self._draw(upper_pipes, lower_pipes, player_y, score)
            self.clock.tick(c.FPS)

    def _draw(self, upper_pipes, lower_pipes, player_y, score):
        sprites = self.sprites
        self.screen.blit(sprites["background"], (0, 0))
        for upper, lower in zip(upper_pipes, lower_pipes):
            self.screen.blit(sprites["pipe"][0], (upper["x"], upper["y"]))
            self.screen.blit(sprites["pipe"][1], (lower["x"], lower["y"]))
        self.screen.blit(sprites["base"], (0, self.ground_y))
        self.screen.blit(sprites["player"], (c.PLAYER_X, player_y))

        digits = [sprites["numbers"][int(d)] for d in str(score)]
        x = (c.SCREEN_WIDTH - sum(d.get_width() for d in digits)) / 2
        for digit in digits:
            self.screen.blit(digit, (x, c.SCREEN_HEIGHT * c.SCORE_Y_RATIO))
            x += digit.get_width()
        pygame.display.update()
