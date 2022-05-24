from math import sin, cos, pi

import pygame

from client.game.src.core.bullet.bullet import Bullet
from client.game.src.utils.config import Config


class BulletController:
    def __init__(self, game):
        self.game = game
        self.bullets = []
        self.consumed_bullets = []

    def add_bullet(self, id, player, position, angle):
        self.bullets.append(Bullet(self.game.screen, id, player, position, angle))

    def draw(self):
        for bullet in self.bullets:
            bullet.draw()

    def get_bullet(self, id):
        for bullet in self.bullets:
            if bullet.id == id:
                return bullet
        return None

    def update_bullets(self, time):
        bullets_ids = []
        for bullet_info in self.game.world_state["bullets"]:
            bullet = self.get_bullet(bullet_info["id"])
            bullets_ids.append(bullet_info["id"])
            position = (bullet_info["x"], bullet_info["y"])
            if bullet:
                # bullet.position = position
                # bullet.angle = bullet_info["angle"]
                self.move(bullet, time)
            else:
                self.add_bullet(
                    bullet_info["id"],
                    self.game.get_player(bullet_info["player_id"]),
                    position,
                    bullet_info["angle"]
                )

        for bullet in self.bullets:
            if bullet.id not in bullets_ids:
                self.consumed_bullets.append(bullet)

        for bullet in self.consumed_bullets:
            self.bullets.remove(bullet)
            self._delete_bullet(bullet)
        self.consumed_bullets.clear()

    def move(self, bullet, time):
        speed = Config.bullet['speed'] * time
        x, y = bullet.position
        radians = -bullet.angle * pi / 180
        new_x = x + (speed * cos(radians))
        new_y = y + (speed * sin(radians))
        bullet.move((new_x, new_y))

        # TODO: Check if additional collision check isn't needed before moving bullet
        if self._collide(bullet):
            self.consumed_bullets.append(bullet)
            # player = self._player_collide(bullet)
            # if player:
            #     if player.lives > 1:
            #         bullet.player.add_hit()
            #         player.was_hit()
            #     else:
            #         bullet.player.add_kill()
            #         player.die()

    @staticmethod
    def _delete_bullet(bullet):
        bullet.delete_sprite()
        del bullet

    def _wall_collide(self, bullet):
        for wall in pygame.sprite.spritecollide(bullet.bullet, self.game.map.walls, False):
            if pygame.sprite.collide_mask(wall, bullet.bullet):
                return True
        return False

    def _player_collide(self, bullet):
        for player in self.game.players:
            if player.is_alive() and pygame.sprite.collide_mask(bullet.bullet, player.tank):
                return player
        return None

    def _collide(self, bullet):
        return self._player_collide(bullet) or self._wall_collide(bullet)

