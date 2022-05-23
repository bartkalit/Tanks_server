import socket
import sys
import json
import pickle
import time
from _thread import *
import threading

from client.game.src.core.screen import Screen
from client.game.src.utils.game_state import GameState

thread_lock = threading.Lock()


def server_read(c, world_state, ):
    print("wczytuje")
    while True:
        b = b''
        data = c.recv(1024)
        b += data
        # print(b)
        # packet = json.loads(b.decode("utf-8"))
        packet = pickle.loads(data)
        thread_lock.acquire()
        world_state["players"] = packet["players"]
        world_state["boosts"] = packet["boosts"]
        world_state["bullets"] = packet["bullets"]
        world_state["boxes"] = packet["boxes"]
        print(packet)
        thread_lock.release()
    c.close()


def tanks(world_state):
    # screen = Screen(world_state)
    # screen.start_game()
    return 0


def server_send(s):
    tps = 3600
    last_time = time.time()
    packet = "client"
    while True:
        data = json.dumps(packet)
        s.send(data.encode("utf-8"))
        interval = tps / 3600.0
        current_time = time.time()
        delta = current_time - last_time

        if delta < interval:
            time.sleep(interval - delta)

        last_time = time.time()


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 3000
    world_state = GameState().world_state

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    start_new_thread(server_read, (s, world_state,))
    start_new_thread(tanks, (world_state, ))
    send = threading.Thread(target=server_send, args=(s,))
    send.start()
    send.join()

    s.close()