import queue
import threading


_log_queue = queue.Queue()
_print_lock = threading.Lock()

def log(msg: str):
    _log_queue.put(msg)

def logger_loop(stop_event):
    while not stop_event.is_set():
        try:
            msg = _log_queue.get(timeout=0.1)
            if msg is None:
                break
            with _print_lock:
                print(msg, flush=True)
        except queue.Empty:
            pass
