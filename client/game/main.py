import time
from _thread import *
import threading

from client.game.src.core.screen import Screen
from client.game.src.utils.game_state import GameState


thread_lock = threading.Lock()


def read(world_state):
    p_id = 0
    ids = [12, 41]
    print(world_state)
    time.sleep(5)
    thread_lock.acquire()
    del world_state["bullets"][0]
    thread_lock.release()
    while p_id != -1:
        for id in ids:
            p_id = id
            x = 1
            y = 0
            angle = 5
            thread_lock.acquire()
            for player_id, player_info in world_state["players"].items():
                if player_id == p_id:
                    player_info["x"] = player_info["x"] + x
                    player_info["y"] = player_info["y"] + y
                    player_info["angle"] = angle
            thread_lock.release()
            time.sleep(0.05)


def game(world_state):
    screen = Screen(world_state)
    screen.start_game()


if __name__ == '__main__':
    world_state = GameState().world_state
    world_state["client_id"] = 12
    start_new_thread(game, (world_state,))
    send = threading.Thread(target=read, args=(world_state,))
    send.start()
    send.join()
