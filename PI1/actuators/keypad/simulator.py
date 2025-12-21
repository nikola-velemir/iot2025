import sys
import termios
import tty

from logger.logger import log

VALID_KEYS = "0123456789ABCD*#"


def _read_key_raw():
    if not sys.stdin.isatty():
        raise RuntimeError("stdin is not a TTY")

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def run_keypad_simulator(keypad_input, stop_event):
    if not sys.stdin.isatty():
        log("[KEYPAD] stdin is not a TTY — simulator disabled")
        return

    log("Keypad ready: 0-9 A-D * # | Press Q to quit")

    while not stop_event.is_set():
        key = _read_key_raw().upper()

        if key == "Q":
            stop_event.set()
            break

        if key in VALID_KEYS:
            keypad_input.press_key(key)