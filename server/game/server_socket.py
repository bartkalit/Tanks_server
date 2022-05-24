import socket
import struct
from _thread import *
import threading
import time
import pickle
import os
from server.game.src.utils.game_state import GameState
from server.game.src.core.screen import Screen

os.environ["SDL_VIDEODRIVER"] = "dummy"
thread_lock = threading.Lock()
clients = []


def client_read(c, id, player_inputs):
    while True:
        if len(clients) < 2:
            continue
        data_size = struct.unpack('>I', c.recv(4))[0]
        b = b''
        reamining_payload_size = data_size

        while reamining_payload_size != 0:
            b += c.recv(reamining_payload_size)
            reamining_payload_size = data_size - len(b)

        try:
            thread_lock.acquire()
            packet = pickle.loads(b)
            player_inputs[id] = packet
        except:
            print("Invalid Packet")
        finally:
            thread_lock.release()
    c.close()


def broadcast(clients, world_state, ):
    tps = 600
    last_time = time.time()
    while True:
        interval = 1 / tps
        current_time = time.time()
        delta = current_time - last_time

        if delta < interval:
            time.sleep(interval - delta)

        if clients:
            for id, client in enumerate(clients):
                thread_lock.acquire()
                world_state["client_id"] = id
                data = pickle.dumps(world_state)
                thread_lock.release()
                client.sendall(struct.pack('>I', len(data)))
                client.sendall(data)
        last_time = time.time()


def game_logic(world_state, player_inputs):
    screen = Screen(world_state, player_inputs)
    pass


def Main():
    ip = socket.gethostbyname(socket.gethostname())
    port = 3000

    print("IP:", ip)
    print("PORT:", port)
    host = ip
    world_state = GameState().world_state
    player_inputs = [GameState().player_input.copy(), GameState().player_input.copy()]
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
