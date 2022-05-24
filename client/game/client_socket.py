import socket
import json
import pickle
from _thread import *
import threading
from pynput.keyboard import Key, Listener, KeyCode

from client.game.src.core.screen import Screen
from client.game.src.utils.game_state import GameState

thread_lock = threading.Lock()


def server_read(c, world_state, ):
    print("wczytuje")
    while True:
        b = b''
        data = c.recv(1024)
        b += data
        try:
            thread_lock.acquire()
            packet = pickle.loads(data)
            world_state["players"] = packet["players"]
            world_state["boosts"] = packet["boosts"]
            world_state["bullets"] = packet["bullets"]
            world_state["boxes"] = packet["boxes"]
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

    def on_press(key):
        if key == KeyCode.from_char('w'):
            inputs["forward"] = True
            server_send(s, inputs)
        elif key == KeyCode.from_char('s'):
            inputs["backward"] = True
            server_send(s, inputs)
        elif key == KeyCode.from_char('a'):
            inputs["left"] = True
            server_send(s, inputs)
        elif key == KeyCode.from_char('d'):
            inputs["right"] = True
            server_send(s, inputs)
        elif key == Key.space:
            inputs["shot"] = True
            server_send(s, inputs)
        elif key == KeyCode.from_char('r'):
            inputs["reload"] = True
            server_send(s, inputs)

    def on_release(key):
        if key == KeyCode.from_char('w'):
            inputs["forward"] = False
            server_send(s, inputs)
        elif key == KeyCode.from_char('s'):
            inputs["backward"] = False
            server_send(s, inputs)
        elif key == KeyCode.from_char('a'):
            inputs["left"] = False
            server_send(s, inputs)
        elif key == KeyCode.from_char('d'):
            inputs["right"] = False
            server_send(s, inputs)
        elif key == Key.space:
            inputs["shot"] = False
            server_send(s, inputs)
        elif key == KeyCode.from_char('r'):
            inputs["reload"] = False
            server_send(s, inputs)

    inputs = GameState().player_input.copy()
    while True:
        with Listener(
                on_press=on_press,
                on_release=on_release) as listener:
            listener.join()
    # while True:
    #     inputs = GameState().player_input.copy()
    #     key = keyboard.read_key()
    #     if key == "w":
    #         print("W")
    #         inputs["forward"] = True
    #         server_send(s, inputs)
    #     elif key == "s":
    #         inputs["backward"] = True
    #         server_send(s, inputs)
    #     elif key == "a":
    #         inputs["left"] = True
    #         server_send(s, inputs)
    #     elif key == "d":
    #         inputs["right"] = True
    #         server_send(s, inputs)
    #     elif key == "space":
    #         inputs["shot"] = True
    #         server_send(s, inputs)
    #     elif key == "r":
    #         inputs["reload"] = True
    #         server_send(s, inputs)




if __name__ == '__main__':
    host = '192.168.0.220'
    port = 3000
    world_state = GameState().world_state

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    start_new_thread(server_read, (s, world_state,))
    # start_new_thread(tanks, (world_state, ))
    send = threading.Thread(target=player_inputs, args=(s,))
    send.start()
    send.join()

    s.close()