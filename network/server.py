import socket
from _thread import *
import threading
import time
import json
import sys

print_lock = threading.Lock()
clients = []


word_state = {
    "players": [
        {
            "id": 41, "x": 5, "y": 2, "angle": 5.0, "lives": 3
        },
        {
            "id": 12, "x": 5, "y": 2, "angle": 5.0, "lives": 3
        }
    ],
    "boosts": [
        {
            "id": 0, "player_id": 0, "x": 0, "y": 0, "angle": 0.0, "active": True, "type": "health"
        },
        {
            "id": 0, "player_id": 0, "x": 0, "y": 0, "angle": 0.0, "active": True, "type": "bullet"
        }
    ],
    "bullets": [
        {
            "id": 0, "player_id": 0, "x": 0, "y": 0, "angle": 0.0
        },
        {
            "id": 1, "player_id": 0, "x": 0, "y": 0, "angle": 0.0
        }
    ]
}
print(sys.getsizeof(word_state))


def client_read(c):
    while True:
        b = b''
        data = c.recv(1024)
        b += data

        packet = json.loads(b.decode("utf-8"))
        print(packet)

    c.close()


def broadcast(clients):
    tps = 3600
    last_time = time.time()

    while True:
        if clients:
            data = json.dumps(word_state)
            for client in clients:
                client.send(data.encode("utf-8"))

        interval = tps / 3600.0
        current_time = time.time()
        delta = current_time - last_time

        if delta < interval:
            time.sleep(interval - delta)

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