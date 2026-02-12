import requests

API_ENDPOINT = "http://192.168.1.2:8080/api/people-changed"


class HttpBackClient:
    def __init__(self, url):
        self.url = url

    def send(self, payload):


        try:
            # Send immediately. This blocks until the server responds.
            response = requests.post(self.url, json=payload, timeout=2)
            if response.status_code == 200:
                print(f"Sent: Success")
            else:
                print(f"Failed to send . Status: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"Error sending to backend: {e}")


if __name__ == "__main__":
    htc = HttpBackClient(API_ENDPOINT)
    payload = {"type":"Left"}
    htc.send(payload)