from client.game.src.utils.config import Config
from client.game.src.utils.sprite import Sprite


class HealthBoost:
    def __init__(self, screen, sprite):
        self.screen = screen
        self._sprite = sprite
        self._reset_time = 0

    def draw(self):
        if not self._reset_time:
            self.screen.blit(self._sprite.image, self._sprite.rect)

    def update_time(self, time):
        self._reset_time -= time
        if self._reset_time <= 0:
            self._reset_time = 0
            self.draw()

    def start_reset(self):
        self._reset_time = Config.boosters['health']['reset_time']

    def get_sprite(self):
        return self._sprite

    def active(self):
        if self._reset_time:
            return False
        return True
