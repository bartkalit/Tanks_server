class GameState:
    world_state = {
        "map": "city",
        "client_id": 12,
        "players": [
            {"id": 41, "x": 400.0, "y": 100.0, "angle": 5.0, "lives": 3},
            {"id": 12, "x": 400.0, "y": 700.0, "angle": 5.0, "lives": 3}
        ],
        "boosts": [
            {"id": 0, "x": 200.0, "y": 100, "active": True, "type": "health"},
            {"id": 1, "x": 200.0, "y": 700, "active": True, "type": "bullet"}
        ],
        "bullets": [
            {"id": 0, "player_id": 41, "x": 650.0, "y": 500.0, "angle": 5.0},
            {"id": 1, "player_id": 12, "x": 100.0, "y": 100.0, "angle": 95.0}
        ],
        "boxes": []
    }

