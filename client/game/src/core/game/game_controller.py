import pygame

from client.game.src.core.game.game import Game
from client.game.src.core.player.player import Player
from client.game.src.core.player.player_controller import PlayerController
from client.game.src.utils.config import Config


class GameController:
    def __init__(self, screen):
        self.screen = screen

        self.game = Game(screen)
        self.game.load_assets()
        self.game.booster_controller.load_boosters()
        self.game.refresh_map()
        self.current_player = None

    def join(self):
        players = self.game.players
        player = Player(self.game, len(players) + 1)
        if self.current_player is None:
            player.change_current()
            self.current_player = PlayerController(player, self.screen)
        self.game.add_player(player)

    def start(self):
        self.game.refresh_map()
        self.loop()

    def loop(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            frame_time = clock.tick(Config.game['fps'])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.current_player.on(frame_time / 1000)
            self.game.bullet_controller.update_bullets(frame_time / 1000)
            self.game.booster_controller.update_time(frame_time / 1000)
            self.game.refresh_map()
            pygame.display.set_caption('FurryTanks - %.2f FPS' % clock.get_fps())
