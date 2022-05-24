class GameState:
    world_state = {
        "map": "city",
        "client_id": 0,
        "players": [],
        "boosts": [],
        "bullets": [],
        "boxes": []
    }

    player_input = {
        "forward": False,
        "backward": False,
        "left": False,
        "right": False,
        "shot": False,
        "reload": False
    }
