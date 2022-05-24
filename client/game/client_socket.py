import socket
import pickle
import struct
from _thread import *
import threading
from pynput.keyboard import Key, Listener, KeyCode

from client.game.src.core.screen import Screen
from client.game.src.utils.game_state import GameState

thread_lock = threading.Lock()
condition_obj = threading.Condition()

def server_read(c, world_state, ):
    print("wczytuje")
    condition_obj.acquire()
    first_packet = True
    while True:
        data_size = struct.unpack('>I', c.recv(4))[0]
        b = b''
        reamining_payload_size = data_size

        while reamining_payload_size != 0:
            b += c.recv(reamining_payload_size)
            reamining_payload_size = data_size - len(b)

        try:
            thread_lock.acquire()
            packet = pickle.loads(b)
            world_state["client_id"] = packet["client_id"]
            world_state["players"] = packet["players"]
            world_state["boosts"] = packet["boosts"]
            world_state["bullets"] = packet["bullets"]
            world_state["boxes"] = packet["boxes"]
            if first_packet:
                condition_obj.notify()
                condition_obj.release()
                first_packet = False
        except:
            print("Invalid Packet")
        finally:
            thread_lock.release()
    c.close()


def tanks(world_state):
    condition_obj.acquire()
    condition_obj.wait(5)
    screen = Screen(world_state)
    condition_obj.release()
    screen.start_game()
    pass


def server_send(s, player_input):
    data = pickle.dumps(player_input)

    s.sendall(struct.pack('>I', len(data)))
    s.sendall(data)


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


if __name__ == '__main__':
    host = "192.168.0.220"
    port = 3000
    world_state = GameState().world_state

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    start_new_thread(server_read, (s, world_state,))
    start_new_thread(tanks, (world_state, ))
    send = threading.Thread(target=player_inputs, args=(s,))
    send.start()
    send.join()

    s.close()