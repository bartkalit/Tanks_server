from server.game.src.core.boosters.boosters import HealthBoost, AmmoBoost


class BoosterController:
    def __init__(self, game):
        self.game = game
        self.active_boosters = []
        self.inactive_boosters = []

    def load_boosters(self):
        for boost_sprite in self.game.map.get_health_boosters():
            self.add_health_booster(boost_sprite)

        for boost_sprite in self.game.map.get_ammo_booster():
            self.add_ammo_booster(boost_sprite)

    def add_health_booster(self, sprite):
        self.active_boosters.append(HealthBoost(self.game.screen, sprite))

    def add_ammo_booster(self, sprite):
        self.active_boosters.append(AmmoBoost(self.game.screen, sprite))

    def draw(self):
        for booster in self.active_boosters:
            booster.draw()

    def update_time(self, time):
        for boost in self.inactive_boosters:
            boost.update_time(time)
            if boost.active():
                self.inactive_boosters.remove(boost)
                self.active_boosters.append(boost)

    def get_active_boosters(self):
        return self.active_boosters

    def pick_up(self, boost, player):
        self.active_boosters.remove(boost)
        self.inactive_boosters.append(boost)
        boost.special_gift(player)
        boost.start_reset()

