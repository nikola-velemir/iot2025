from shared.logger.logger import log

VALID_KEYS = "0123456789ABCD*#"

DEBOUNCE_TIME = 0.2  # seconds


def simulated_keypad_input_loop(keypad_input, stop_event):
    log("Keypad ready: enter keys (0-9 A-D * #). Type Q to quit.")

    while not stop_event.is_set():
        try:
            line = input("> ").strip().upper()
        except (EOFError, KeyboardInterrupt):
            stop_event.set()
            break

        if not line:
            continue

        if line == "Q":
            stop_event.set()
            break

        if len(line) == 1 and line in VALID_KEYS:
            keypad_input.press_key(line)
            log(f"[KEYPAD] Key pressed: {line}")
        else:
            # Explicitly ignore everything else
            log(f"[KEYPAD] Ignored input: '{line}'")