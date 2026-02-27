import signal
import sys
import threading

from shared.sensors.webc.sensor import WebCamera


def run_webc(config,stop_event):
    if config['simulated']:
        return None

    camera = WebCamera(
        port=config.get("port", 8080),
        bind_address=config.get("bind_address", "0.0.0.0")
    )

    camera.run()

    def watcher():
        stop_event.wait()
        camera.stop()

    t = threading.Thread(target=watcher, daemon=True)
    t.start()

    return camera