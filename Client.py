import socket
import pickle
import threading
import logging
import contextlib
import time
import queue


class Client:
    action_queue = queue.Queue()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    input_thread = None

    def send_object(self, obj):
        if self.input_thread is not None and self.input_thread.is_alive():
            self.client_socket.sendall(pickle.dumps(obj))
            return True
        else:
            return False

    def handler(self):
        while True:
            try:
                data = self.client_socket.recv(4096)
            except ConnectionError as e:
                logging.error("Disconnect from server")
                break
            if not data:
                logging.error("Disconnect from server")
                raise ConnectionError("Disconnect from server")
            obj = pickle.loads(data)
            logging.debug("Object {} received".format(str(obj)))
            self.action_queue.put(obj)

    def __init__(self, addr, port=8080):
        self.addr = addr
        self.port = port

    def run(self):
        self.client_socket.connect((self.addr, self.port))
        self.input_thread = threading.Thread(target=self.handler)
        self.input_thread.daemon = True
        self.input_thread.start()


def reconnect_client_thread(client):
    while True:
        if client.input_thread is None:
            logging.debug("Starting client")
            client.run()
        else:
            if client.input_thread.is_alive():
                time.sleep(1)
            else:
                logging.warning("client_thread fallen - try to reconnect")
                try:
                    client.run()
                except OSError as e:
                    logging.error("Couldn't connect to server - {}".format(e))
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
        our_client.send_object([1,1,1,1,1,1])