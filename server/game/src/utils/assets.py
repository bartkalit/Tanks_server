import pygame

from server.game.src.utils.blocks import Blocks
from server.game.src.utils.config import Config
from server.game.src.utils.sprite import Sprite


class Assets:
    all = {}
    width = 0
    height = 0

    def __init__(self, screen, map):
        self.screen = screen
        self.map = map
        self.load_assets()

    def load_assets(self):
        assets = Blocks.getAll()

        (w, h) = self.screen.get_size()
        self.width = w / self.map.width
        self.height = (h - Config.screen['stat_bar']) / self.map.height
        for asset in assets:
            self.all[asset] = pygame.image.load('assets/textures/' + asset + '.png')
            self.all[asset] = pygame.transform.scale(self.all[asset], (self.width, self.height))

    def set_wall(self, position):
        self.map.add_wall(Sprite(position, self.all[Blocks.wall]))

    def set_ground(self, position):
        self.map.add_ground(Sprite(position, self.all[Blocks.ground]))

    def set_spawn_point(self, position):
        self.map.add_spawn_point(position)
        self.map.add_ground(Sprite(position, self.all[Blocks.ground]))

    def set_health_boost(self, position):
        self.set_ground(position)
        self.map.add_health_boost(Sprite(position, self.all[Blocks.health_boost]))

    def set_ammo_boost(self, position):
        self.set_ground(position)
        self.map.add_ammo_boost(Sprite(position, self.all[Blocks.ammo_boost]))

    def set_block(self, char, position):
        block = Blocks.getBlock(char)
        if block == Blocks.wall:
            self.set_wall(position)
        if block == Blocks.ground:
            self.set_ground(position)
        if block == Blocks.spawn_point:
            self.set_spawn_point(position)
        if block == Blocks.health_boost:
            self.set_health_boost(position)
        if block == Blocks.ammo_boost:
            self.set_ammo_boost(position)
