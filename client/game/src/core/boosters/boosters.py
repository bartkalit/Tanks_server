from client.game.src.utils.config import Config
from client.game.src.utils.sprite import Sprite


class HealthBoost:
    def __init__(self, screen, id, sprite):
        self.screen = screen
        self.id = id
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

    @staticmethod
    def special_gift(player):
        player.add_health(Config.boosters['health']['lives'])


class AmmoBoost:
    def __init__(self, screen, id, sprite):
        self.screen = screen
        self.id = id
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
        self._reset_time = Config.boosters['ammo']['reset_time']

    def get_sprite(self):
        return self._sprite

    def active(self):
        if self._reset_time:
            return False
        return True

    @staticmethod
    def special_gift(player):
        player.add_ammo(Config.boosters['ammo']['bullets'])
