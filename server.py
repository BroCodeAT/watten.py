import socket
from typing import Dict


class NetworkServer(socket.socket):
    def __init__(self, host: str = "127.0.0.1", port: int = 3333):
        self.clients: Dict[socket.socket] = {}

        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        print(f"[{'LISTENING':<10}] Bound to the port: {host}:{port}")
        self.bind((host, port))

    def accept_clients(self, amount: int = 4):
        self.listen(4)
        for i in range(amount):
            conn, addr = self.accept()

            name = conn.recv(1024).decode()
            self.clients[addr] = {
                "name": name,
                "connection": conn
            }
            print(f"[{'CONNECTION':<10}] {name} connected to the Game {i + 1}/{amount}")


if __name__ == '__main__':
    server = NetworkServer()
    server.accept_clients()


