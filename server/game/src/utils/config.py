class Config:
    player = {
        'speed': {
            'drive': {
                'forward': 120,
                'backward': 70
            },
            'rotate': 80
        },
        'tank': {
            'scale': 0.7,
            'magazine': 5,
            'reload_bullet': 3,
            'reload_magazine': 10
        },
        'lives': 3
    }

    game = {
        'fps': 60
    }

    bullet = {
        'speed': 40,
        'scale': 0.09
    }

    screen = {
        'resolution': {
            'width': 800,
            'height': 800
        },
        'stat_bar': 80
    }

    rewards = {
        'hit': 25,
        'kill': 200
    }

    boosters = {
        'health': {
            'lives': 1,
            'reset_time': 5
        },
        'ammo' : {
            'bullets': 2,
            'reset_time': 10
        }

    }
