from RPi import GPIO

_initialized = False

def ensure_gpio_initialized():
    global _initialized
    if not _initialized:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        _initialized = True
