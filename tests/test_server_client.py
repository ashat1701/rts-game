import os
from MainMenu import run_server
import multiprocessing
from queue import Queue
import time
os.chdir("..")

def f(test):
    st = time.time()
    test()
queue = Queue()

def test_map_receive():
    server_thread = multiprocessing.Process(target=run_server,
                                            args=["Singleplayer"])
    server_thread.start()
    time.sleep(3)
    from src.Client.SIOServer import sio, run
    sio.on("message")(on_message)
    sio.on("disconnect")(on_disconnect)
    run("localhost")
    assert queue.get()[0] == "MAP"
    server_thread.terminate()

def on_message(data):
    queue.put(data)

def on_disconnect():
    print("disco")
    exit(0)

