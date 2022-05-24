class GameState:
    world_state = {
        "map": "danzig",
        "client_id": 0,
        "players": [],
        "boosts": [],
        "bullets": [],
        "boxes": [],
        "ready": False
    }

    player_input = {
        "forward": False,
        "backward": False,
        "left": False,
        "right": False,
        "shot": False,
        "reload": False
    }
