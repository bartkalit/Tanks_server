import threading

import pygame

from client.game.src.core.game.game import Game
from client.game.src.core.player.player import Player
from client.game.src.core.player.player_controller import PlayerController
from client.game.src.core.stat_bar.stat_bar import StatBar
from client.game.src.utils.config import Config

thread_lock = threading.Lock()


class GameController:
    def __init__(self, screen, world_state):
        self.screen = screen
        self.world_state = world_state
        self.game = Game(screen, world_state)
        self.game.load_players()
        self.game.load_assets()
        self.game.refresh_map()
        self.current_player = None

    def join(self):
        print(self.game.world_state["client_id"])
        player = self.game.get_player(self.game.world_state["client_id"])
        if self.current_player is None:
            player.change_current()
            self.current_player = PlayerController(player, self.screen)
        pass

    def start(self):
        self.game.refresh_map()
        self.loop()

    def loop(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            frame_time = clock.tick(Config.game['fps'])
            thread_lock.acquire()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            # self.current_player.on(frame_time / 1000)
            self.game.bullet_controller.update_bullets(frame_time / 1000)
            # self.game.booster_controller.update_time()
            self.game.update_players(self.current_player.player)
            if self.world_state['ready']:
                self.game.refresh_map()
            else:
                StatBar.show_waiting(self.screen)
            thread_lock.release()
            pygame.display.set_caption('FurryTanks - %.2f FPS' % clock.get_fps())
