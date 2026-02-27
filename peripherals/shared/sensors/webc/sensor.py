import subprocess
import signal
import sys


class WebCamera:
    def __init__(self, port=8080, bind_address="0.0.0.0"):
        self.port = port
        self.bind_address = bind_address
        self._process = None

    def run(self):
        cmd = [
            "mjpg_streamer",
            "-i", "input_uvc.so",
            "-o",
            f"output_http.so -p {self.port} -l {self.bind_address} "
            "-w /usr/local/share/mjpg-streamer/www"
        ]

        self._process = subprocess.Popen(cmd)
        print(f"mjpg_streamer started on {self.bind_address}:{self.port}")

    def stop(self):
        if self._process and self._process.poll() is None:
            print("Stopping mjpg_streamer...")
            self._process.terminate()
            try:
                self._process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("Force killing mjpg_streamer...")
                self._process.kill()


