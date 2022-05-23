import socket
import sys
import json
import pickle
import time
from _thread import *
import threading
import keyboard

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
        try:
            thread_lock.acquire()
            packet = pickle.loads(data)
            world_state["players"] = packet["players"]
            world_state["boosts"] = packet["boosts"]
            world_state["bullets"] = packet["bullets"]
            world_state["boxes"] = packet["boxes"]
            # print(packet)
        except:
            print("Invalid Packet")
        finally:
            thread_lock.release()
    c.close()


def tanks(world_state):
    screen = Screen(world_state)
    screen.start_game()
    pass


def server_send(s, player_input):
    data = json.dumps(player_input)
    s.send(data.encode("utf-8"))


def player_inputs(s, ):
    while True:
        inputs = GameState().player_input.copy()
        key = keyboard.read_key()
        if key == "w":
            print("W")
            inputs["forward"] = True
            server_send(s, inputs)
        if key == "s":
            inputs["backward"] = True
            server_send(s, inputs)
        if key == "a":
            inputs["left"] = True
            server_send(s, inputs)
        if key == "d":
            inputs["right"] = True
            server_send(s, inputs)
        if key == "space":
            inputs["shot"] = True
            server_send(s, inputs)
        if key == "r":
            inputs["reload"] = True
            server_send(s, inputs)


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 3000
    world_state = GameState().world_state

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    start_new_thread(server_read, (s, world_state,))
    # start_new_thread(player_inputs, (s,))
    start_new_thread(tanks, (world_state, ))
    send = threading.Thread(target=player_inputs, args=(s,))
    send.start()
    send.join()

    s.close()