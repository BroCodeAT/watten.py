import socket
from typing import Dict

HOST = "127.0.0.1"
PORT = 3333
ENCODING = "utf-8"


class NetworkServer(socket.socket):
    def __init__(self, host: str = "127.0.0.1", port: int = 3333):
        self.clients: Dict = {}

        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        print(f"[{'LISTENING':<10}] Bound to the port: {host}:{port}")
        self.bind((host, port))

    def accept_clients(self, amount: int = 4):
        self.listen(4)
        for i in range(amount):
            conn, addr = self.accept()

            name = conn.recv(1024).decode(ENCODING)
            self.clients[addr] = {
                "name": name,
                "connection": conn
            }
            print(f"[{'CONNECTION':<10}] {name} connected to the Game {i + 1}/{amount}")

    def send_all(self, data: str):
        for addr in self.clients:
            self.clients[addr]["connection"].send(data.encode(ENCODING))

    def send_to(self, data: str, addr: str):
        if addr not in self.clients:
            return None

        self.clients[addr]["connection"].send(data.encode(ENCODING))

    def receive(self, addr: str):
        if addr not in self.clients:
            return None

        return self.clients[addr]["connection"].receive().decode(ENCODING)


if __name__ == '__main__':
    server = NetworkServer(host=HOST, port=PORT)
    server.accept_clients()


