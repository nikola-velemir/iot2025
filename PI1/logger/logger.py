import queue
import threading
import time

_log_queue = queue.Queue()

def log(msg: str):
    _log_queue.put(msg)

def logger_loop(stop_event):
    while not stop_event.is_set():
        try:
            msg = _log_queue.get(timeout=0.01)
            print(msg)
        except queue.Empty:
            pass
