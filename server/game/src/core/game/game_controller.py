import pygame

from server.game.src.core.game.game import Game
from server.game.src.core.player.player import Player
from server.game.src.core.player.player_controller import PlayerController
from server.game.src.utils.config import Config


class GameController:
    def __init__(self, screen, world_state, players_inputs):
        self.screen = screen
        self.world_state = world_state
        self.players_inputs = players_inputs
        self.game = Game(screen, world_state, players_inputs)
        self.game.load_assets()
        self.game.booster_controller.load_boosters()
        self.game.refresh_map()
        self.players = []
        self.current_player = None

    def join(self):
        players = self.game.players
        player = Player(self.game, len(players))
        self.players.append(PlayerController(player, self.screen, self.players_inputs))
        if self.current_player is None:
            player.change_current()
            self.current_player = PlayerController(player, self.screen, self.players_inputs)
        self.game.add_player(player)

    def start(self):
        self.game.refresh_map()
        self.loop()

    def get_players_info(self):
        players = []
        for player in self.game.players:
            players.append(player.get_info())
        return players

    def get_bullets_info(self):
        bullets = []
        for bullet in self.game.bullet_controller.bullets:
            bullets.append(bullet.get_info())
        return bullets

    def loop(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            frame_time = clock.tick(Config.game['fps'])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            for player in self.players:
                player.on(frame_time / 1000)
            # self.current_player.on(frame_time / 1000)
            self.world_state["players"] = self.get_players_info()
            self.game.bullet_controller.update_bullets(frame_time / 1000)
            self.world_state["bullets"] = self.get_bullets_info()
            self.game.booster_controller.update_time(frame_time / 1000)
            self.game.refresh_map()
            pygame.display.set_caption('FurryTanks - %.2f FPS' % clock.get_fps())
