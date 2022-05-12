import socket
import sys
import json
import time
from _thread import *
import threading

thread_lock = threading.Lock()

player = {"id": 0, "x": 5, "y": 2, "angle": 5.0, "lives": 3}
bullet = {"id": 0, "player_id": 0, "x": 0, "y": 0, "angle": 0.0}
boost = {"id": 0, "x": 0, "y": 0, "type": 0}
box = {"id": 0, "x": 0, "y": 0}


packet = {
    "players": [
        {
            "id": 0, "x": 5, "y": 2, "angle": 5.0, "lives": 3
        },
        {
            "id": 0, "x": 5, "y": 2, "angle": 5.0, "lives": 3
        }]
}


def server_read(c):
    while True:
        b = b''
        data = c.recv(1024)
        b += data


        packet = json.loads(b.decode("utf-8"))
        print(packet)
        # print(b.decode("utf-8"))

    c.close()


def server_send(s):
    tps = 3600
    last_time = time.time()

    while True:
        data = json.dumps(packet)
        s.send(data.encode("utf-8"))
        if not data:
            thread_lock.release()
        interval = tps / 3600.0
        current_time = time.time()
        delta = current_time - last_time

        if delta < interval:
            time.sleep(interval - delta)

        last_time = time.time()


def Main():
    host = '127.0.0.1'
    port = 3000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    thread_lock.acquire()
    start_new_thread(server_read, (s,))
    send = threading.Thread(target=server_send, args=(s,))
    send.start()
    send.join()


    s.close()


if __name__ == '__main__':
    Main()