import socket
from _thread import *
import threading
import time
import json
import pickle

from client.game.src.utils.game_state import GameState

thread_lock = threading.Lock()
clients = []


def client_read(c):
    while True:
        b = b''
        data = c.recv(1024)
        b += data

        packet = json.loads(b.decode("utf-8"))
        # print(packet)
    c.close()


def broadcast(clients):
    tps = 20
    last_time = time.time()
    world_state = GameState().world_state
    while True:
        interval = 1 / tps
        current_time = time.time()
        delta = current_time - last_time

        if delta < interval:
            time.sleep(interval - delta)

        if clients:
            thread_lock.acquire()
            print((time.time() - last_time) * 120)
            world_state["players"][1]["x"] += 80 * (time.time() - last_time)
            world_state["players"][0]["x"] += 80 * (time.time() - last_time)
            world_state["players"][1]["angle"] += 0.5
            thread_lock.release()
            print("wysylam")
            # data = json.dumps(world_state)
            data = pickle.dumps(world_state)
            for client in clients:
                # client.send(data.encode("utf-8"))
                client.send(data)
        last_time = time.time()


def Main():
    host = "127.0.0.1"

    port = 3000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)
    s.listen(5)
    start_new_thread(broadcast, (clients,))
    while True:
        c, addr = s.accept()
        clients.append(c)
        print('Connected to :', addr[0], ':', addr[1])

        start_new_thread(client_read, (c,))

    s.close()


if __name__ == '__main__':
    Main()