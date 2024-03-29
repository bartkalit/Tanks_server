import pygame

from client.game.src.utils.sprite import BulletSprite


class Bullet:
    def __init__(self, screen, id, player, position, angle):
        self.screen = screen
        self.id = id
        self.player = player
        self.bullet = None
        self.position = position
        self.angle = angle
        self.create()

    def create(self):
        print(f"id {self.id} pos {self.position} ang {self.angle}")
        self.bullet = BulletSprite(self.position, self.angle)

    def draw(self):
        self.screen.blit(self.bullet.image, self.bullet.rect)

    def move(self, position):
        self.position = position
        self.bullet.move(position)

    def delete_sprite(self):
        del self.bullet
