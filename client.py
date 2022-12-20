import json
import time
import socket
import multiprocessing

HOST = "127.0.0.2"
PORT = 3333
FORMAT = "utf-8"


class NetworkClient:

    def __init__(self):
        self.lock = multiprocessing.Lock()
        self.que = multiprocessing.Queue()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener = multiprocessing.Process(target=self.recv_in_process)
        self.running: bool = True

    def server_connect(self, name: str, host: str = "127.0.0.2", port: int = 3333):
        self.server.connect((host, port))
        with self.lock:
            self.server.send(name.encode())
        resp = self.recv_from_server()
        print(resp)
        if resp.get("command") == "CONNECTED":
            if resp.get("name") == name:
                self.listener.start()

    def send_to_server(self, msg: str):
        to_send = msg.encode(FORMAT)
        with self.lock:
            self.server.send(to_send)

    def recv_from_server(self):
        with self.lock:
            data = self.server.recv(1024).decode()
        print("data:", data)
        try:
            return json.loads(data)
        except json.decoder.JSONDecodeError:
            pass

    def recv_in_process(self):
        time.sleep(5)
        while self.running:
            recv = self.recv_from_server()
            if recv:
                self.que.put(recv)
