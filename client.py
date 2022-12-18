import json
import queue
import socket
import threading

HOST = "127.0.0.2"
PORT = 3333
FORMAT = "utf-8"


class NetworkClient(socket.socket):

    def __init__(self):
        self.que = queue.Queue()
        self.listener = threading.Thread(target=self.recv_in_process)
        self.running: bool = True
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)

    def server_connect(self, name: str, host: str = "127.0.0.2", port: int = 3333):
        self.connect((host, port))
        self.send(name.encode())
        self.listener.start()

    def send_to_server(self, msg: str):
        to_send = msg.encode(FORMAT)
        self.send(to_send)

    def recv_from_server(self):
        data = self.recv(1024).decode()
        try:
            return json.loads(data)
        except json.decoder.JSONDecodeError:
            pass

    def recv_in_process(self):
        while self.running:
            recv = self.recv_from_server()
            self.que.put(recv)

