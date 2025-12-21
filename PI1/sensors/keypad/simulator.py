import select
import sys
import termios
import time
import tty

from logger.logger import log

VALID_KEYS = "0123456789ABCD*#"

DEBOUNCE_TIME = 0.2  # seconds



def simulated_keypad_input_loop(keypad_input, stop_event):

    if not sys.stdin.isatty():
        log("[KEYPAD] stdin is not a TTY — simulator disabled")
        return

    log("Keypad ready: 0-9 A-D * # | Press Q to quit")

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setcbreak(fd)

    last_press_time = 0

    try:
        while not stop_event.is_set():
            if sys.stdin in select.select([sys.stdin], [], [], 0.1)[0]:
                key = sys.stdin.read(1).upper()

                if key == "Q":
                    stop_event.set()
                    break

                now = time.time()
                if key in VALID_KEYS and (now - last_press_time) >= DEBOUNCE_TIME:
                    last_press_time = now
                    keypad_input.press_key(key)
                    log(f"[KEYPAD] Key pressed: {key}")

                time.sleep(DEBOUNCE_TIME)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
