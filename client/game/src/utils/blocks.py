class Blocks:
    wall = 'wall'
    ground = 'ground'
    spawn_point = 'spawn'
    health_boost = 'health_booster'
    ammo_boost = 'ammo_booster'

    @staticmethod
    def getAll():
        return {Blocks.wall, Blocks.ground, Blocks.health_boost, Blocks.ammo_boost}

    @staticmethod
    def getBlock(char):
        if char == '#':
            return Blocks.wall
        if char == 'S':
            return Blocks.spawn_point
        else:
            return Blocks.ground
        # if char == 'H':
        #     return Blocks.health_boost
        # if char == 'A':
        #     return Blocks.ammo_boost
