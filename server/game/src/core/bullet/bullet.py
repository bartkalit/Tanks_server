import pygame

from server.game.src.utils.sprite import BulletSprite


class Bullet:
    def __init__(self, screen, player, position, angle, id):
        self.screen = screen
        self.player = player
        self.bullet = None
        self.position = position
        self.angle = angle
        self.id = id
        self.create()

    def create(self):
        self.bullet = BulletSprite(self.position, self.angle)

    def draw(self):
        self.screen.blit(self.bullet.image, self.bullet.rect)

    def move(self, position):
        self.position = position
        self.bullet.move(position)

    def delete_sprite(self):
        del self.bullet

    def get_info(self):
        x, y = self.position
        return {"id": self.id, "player_id": self.player.id, "x": x, "y": y, "angle": self.angle}
