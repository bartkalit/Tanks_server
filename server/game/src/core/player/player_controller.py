from enum import Enum
from math import cos, sin, pi
import pygame

from server.game.src.core.stat_bar.stat_bar import StatBar
from server.game.src.utils.config import Config


class Drive(Enum):
    FORWARD = 0
    BACKWARD = 1


class Rotate(Enum):
    LEFT = 0
    RIGHT = 1


class PlayerController:
    def __init__(self, player, screen, players_inputs):
        self.screen = screen
        self.player = player
        self.players_inputs = players_inputs
        self.draw_ui()

    def draw_ui(self):
        StatBar.show_avatar(self.screen)
        StatBar.show_lives(self.screen, self.player)
        StatBar.show_magazine(self.screen, self.player)
        StatBar.show_points(self.screen, self.player)

    def on(self, time):
        if self.player.is_alive():
            input = self.players_inputs[self.player.id - 1]
            if input["forward"]:
                self.drive(Drive.FORWARD, time)
            if input["backward"]:
                self.drive(Drive.BACKWARD, time)
            if input["left"]:
                self.rotate(Rotate.LEFT, time)
            if input["right"]:
                self.rotate(Rotate.RIGHT, time)
            if input["shot"]:
                self.shot()
            if input["reload"]:
                self._reload_magazine()
            if self.player.reload_time > 0:
                self._reload(time)

    def _reload(self, time):
        self.player.reload_time -= time
        StatBar.show_reload(self.screen, self.player)
        if self.player.reload_time <= 0:
            if self.player.bullets == 0:
                self._reload_magazine()
            StatBar.show_magazine(self.screen, self.player)

    def _reload_magazine(self):
        if self.player.bullets != Config.player['tank']['magazine']:
            self.player.reload_magazine()

    def _start_reload_time(self):
        self.player.reload_time = Config.player['tank']['reload_magazine']

    def drive(self, drive: Drive, time):
        x, y = self.player.position
        radians = -self.player.angle * pi / 180
        if drive == Drive.FORWARD:
            speed = Config.player['speed']['drive']['forward'] * time
            new_x = x + (speed * cos(radians))
            new_y = y + (speed * sin(radians))
        else:
            speed = Config.player['speed']['drive']['backward'] * time
            new_x = x - (speed * cos(radians))
            new_y = y - (speed * sin(radians))

        new_position = (new_x, new_y)
        self.player.move(new_position)
        # TODO: Send new position to the server

    def rotate(self, angle: Rotate, time):
        rotate_speed = Config.player['speed']['rotate'] * time
        if angle == Rotate.LEFT:
            new_angle = rotate_speed
        else:
            new_angle = -rotate_speed

        if new_angle > 360:
            new_angle -= 360
        elif new_angle < -360:
            new_angle += 360

        self.player.rotate(new_angle)
        # TODO: Send new angle to the server

    def shot(self):
        if self.player.reload_time <= 0:
            self.player.reload_time = Config.player['tank']['reload_bullet']
            if self.player.bullets - 1 == 0:
                self._start_reload_time()
            self.player.shot()
            StatBar.show_magazine(self.screen, self.player)
            # TODO: Send bullet position to the server
