import socket
from _thread import *
import threading
import time
import json
import pickle

from server.game.src.utils.game_state import GameState
from server.game.src.core.screen import Screen

thread_lock = threading.Lock()
clients = []


def client_read(c, id, player_inputs):
    while True:
        b = b''
        data = c.recv(1024)
        b += data
        try:
            thread_lock.acquire()
            packet = json.loads(b.decode("utf-8"))
            player_inputs[id] = packet
        except:
            print("Invalid Packet")
        finally:
            thread_lock.release()
    c.close()


def broadcast(clients, world_state, ):
    tps = 30
    last_time = time.time()
    while True:
        interval = 1 / tps
        current_time = time.time()
        delta = current_time - last_time

        if delta < interval:
            time.sleep(interval - delta)

        if clients:
            thread_lock.acquire()
            data = pickle.dumps(world_state)
            thread_lock.release()
            for client in clients:
                client.send(data)
        last_time = time.time()


def game_logic(world_state, player_inputs):
    screen = Screen(world_state, player_inputs)
    pass


def Main():
    host = "192.168.0.220"
    world_state = GameState().world_state
    player_inputs = [GameState().player_input.copy(), GameState().player_input.copy()]
    port = 3000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)
    s.listen(5)
    start_new_thread(game_logic, (world_state, player_inputs,))
    start_new_thread(broadcast, (clients, world_state))

    id = 0
    while True:
        c, addr = s.accept()
        clients.append(c)
        print('Connected to :', addr[0], ':', addr[1])
        start_new_thread(client_read, (c, id, player_inputs))
        id += 1

    s.close()


if __name__ == '__main__':
    Main()
