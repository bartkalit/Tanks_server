import pygame

from client.game.src.core.boosters.booster_controller import BoosterController
from client.game.src.core.bullet.bullet_controller import BulletController
from client.game.src.core.map import Map
from client.game.src.core.player.player import Player
from client.game.src.utils.assets import Assets


class Game:
    def __init__(self, screen, world_state):
        self.screen = screen
        self.world_state = world_state
        self.map = self._load_map(world_state["map"])
        self.players = []
        self.assets = Assets(screen, self.map)
        self.bullet_controller = BulletController(self)
        self.booster_controller = BoosterController(self)
        pass

    def get_player(self, id):
        for player in self.players:
            if player.id == id:
                return player

    # def add_player(self, player):
    #     self.players.append(player)
    #
    #
    #     # players = self.game.players
    #     # player = Player(self.game, len(players) + 1)
    #     # if self.current_player is None:
    #     #     player.change_current()
    #     #     self.current_player = PlayerController(player, self.screen)
    #     # self.game.add_player(player)

    def load_assets(self):
        x, y = 0, 0
        for row in self.map.data:
            x = 0
            for block in row:
                self.assets.set_block(block, (x, y))
                x += self.assets.width
            y += self.assets.height

    def load_players(self):
        for player_info in self.world_state["players"]:
            position = (player_info["x"], player_info["y"])
            player = Player(self, player_info["id"], position, player_info["angle"])
            self.players.append(player)

    def update_players(self):
        for player_info in self.world_state["players"]:
            id = player_info["id"]
            position = (player_info["x"], player_info["y"])
            player = self.get_player(id)
            player.move(position)
            player.rotate(player_info["angle"])
            player.lives = player_info["lives"]
            if player.points != player_info["points"]:
                player.points = player_info["points"]
                player.update_points_ui()

    def refresh_map(self):
        self.refresh_ground()
        self.refresh_walls()
        self.refresh_boosters()
        self.refresh_players()
        # self.refresh_bullets()
        pygame.display.update()

    def refresh_ground(self):
        self.map.ground.draw(self.screen)

    def refresh_walls(self):
        self.map.walls.draw(self.screen)

    def refresh_players(self):
        for player in self.players:
            player.draw()
        self.refresh_bullets()
        pygame.display.update()

    def refresh_bullets(self):
        self.bullet_controller.draw()

    def refresh_boosters(self):
        self.booster_controller.draw()

    def _load_map(self, map_name: str) -> Map:
        try:
            map = open('assets/maps/' + map_name + '.map')
            lines = map.readlines()
            y = len(lines)
            x = 0
            data = []
            for line in lines:
                line = line.replace('\n', '')
                data.append(line)

                if x == 0:
                    x = len(line)
                elif len(line) != x:
                    raise Exception('Invalid map data')
            return Map(map_name, x, y, data)
        except ValueError:
            print(ValueError)

        return None
