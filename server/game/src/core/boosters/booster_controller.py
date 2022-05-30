from server.game.src.core.boosters.boosters import HealthBoost, AmmoBoost


class BoosterController:
    def __init__(self, game, world_state):
        self.game = game
        self.world_state = world_state
        self.active_boosters = []
        self.inactive_boosters = []

    def load_boosters(self):
        boosters = []
        counter = 0
        for boost_sprite in self.game.map.get_health_boosters():
            boosters.append(
                {"id": counter, "x": boost_sprite.rect.x, "y": boost_sprite.rect.y, "active": True, "type": "health"})
            self.add_health_booster(boost_sprite, counter)
            counter += 1

        for boost_sprite in self.game.map.get_ammo_booster():
            boosters.append(
                {"id": counter, "x": boost_sprite.rect.x, "y": boost_sprite.rect.y, "active": True, "type": "bullet"})
            self.add_ammo_booster(boost_sprite, counter)
            counter += 1
        self.world_state["boosts"] = boosters

    def add_health_booster(self, sprite, id):
        self.active_boosters.append(HealthBoost(self.game.screen, sprite, id))

    def add_ammo_booster(self, sprite, id):
        self.active_boosters.append(AmmoBoost(self.game.screen, sprite, id))

    def draw(self):
        for booster in self.active_boosters:
            booster.draw()

    def update_time(self, time):
        for boost in self.inactive_boosters:
            boost.update_time(time)
            if boost.active():
                self.inactive_boosters.remove(boost)
                self.active_boosters.append(boost)
                for boost_info in self.world_state["boosts"]:
                    if boost_info["id"] == boost.id:
                        boost_info["active"] = True

    def get_active_boosters(self):
        return self.active_boosters

    def pick_up(self, boost, player):
        self.active_boosters.remove(boost)
        self.inactive_boosters.append(boost)
        for boost_info in self.world_state["boosts"]:
            if boost_info["id"] == boost.id:
                boost_info["active"] = False
        boost.special_gift(player)
        boost.start_reset()

