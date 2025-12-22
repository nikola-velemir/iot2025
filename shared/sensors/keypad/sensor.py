from shared.sensors.keypad.input import KeypadInput
from shared.logger.logger import log


class KeyPad:
    def __init__(self, keypad: KeypadInput):
        self.keypad = keypad

    def on_key_pressed(self, key: str):
        log(f"[KEYPAD] Key pressed: {key}")

    def poll(self):
        key = self.keypad.read_key()
        if key:
            self.on_key_pressed(key)