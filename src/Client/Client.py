import socket
import pickle
import threading
import logging
import contextlib
import time
import queue
from src.utility.constants import PORT


class Client:
    action_queue = queue.Queue()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    input_thread = None
    current_id = None
    buffer  = b""
    length = None
    def send_object(self, obj):
        if (self.input_thread is not None and self.input_thread.is_alive()) or self.current_id is None:
            self.client_socket.sendall(pickle.dumps((self.current_id, obj)))
            return True
        else:
            return False

    def handler(self):
        while True:
            try:
                data = self.client_socket.recv(8192)
            except ConnectionError as e:
                logging.error("Disconnect from server")
                break
            if not data:
                logging.error("Disconnect from server")
                break
            obj = pickle.loads(data)
            if (obj == "START_GAME"):
                self.game_started = True
            else:
                self.action_queue.put(obj)

    def __init__(self, addr, port=PORT):
        self.addr = addr
        self.port = port
        self.game_started = False
    def run(self):
        self.client_socket.connect((self.addr, self.port))
        logging.debug("connected")
        if self.current_id is None:
            self.get_new_id_()
        else:
            self.get_reconnect_id()
        self.input_thread = threading.Thread(target=self.handler)
        self.input_thread.daemon = True
        self.input_thread.start()

    def get_new_id_(self):
        action = "ACTION_GET_ID"
        self.send_object(action)
        id_bytes = self.client_socket.recv(4096)
        id = pickle.loads(id_bytes)
        self.current_id = id

    def get_reconnect_id(self):
        action = "ACTION_RECONNECT:" + str(self.current_id)
        self.send_object(action)
        id_bytes = self.client_socket.recv(4096)
        id = pickle.loads(id_bytes)
        self.current_id = id

    def receive_map(self, size):
        map = []
        for i in range(size):
            lvl = self.action_queue.get()
            map.append(lvl)
        self.send_object("MAP_RECEIVED")
        return map


def close_socket(connection):
    try:
        connection.shutdown(socket.SHUT_RDWR)
    except:
        pass
    try:
        connection.close()
    except:
        pass

def reconnect_client_thread(client):
    while True:
        if client.input_thread is None:
            logging.debug("Starting client")
            try:
                client.run()
            except (OSError, ConnectionError) as e:
                logging.error("Couldn't connect to server - {}".format(e))
                time.sleep(1)
            except Exception as e:
                logging.error("Undefined exception - {}".format(e))
                time.sleep(1)
        else:
            if client.input_thread.is_alive():
                time.sleep(1)
            else:
                logging.warning("client_thread fallen - try to reconnect")
                try:
                    client.run()
                except (OSError, ConnectionError) as e:
                    logging.error("Couldn't connect to server - {}".format(e))
                    time.sleep(1)
                except Exception as e:
                    logging.error("Undefined exception - {}".format(e))
                    time.sleep(1)


@contextlib.contextmanager
def reconnecting_client(addr, port=8080):
    client = Client(addr, port)
    new_thread = threading.Thread(target=reconnect_client_thread, args=[client])
    new_thread.daemon = True
    new_thread.start()
    while True:
        if client.input_thread is not None:
            break
        time.sleep(0.1)
    try:
        yield client
    finally:
        client.client_socket.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    with reconnecting_client("127.0.0.1") as our_client:
        our_client.send_object([1, 1, 1, 1, 1, 1])
