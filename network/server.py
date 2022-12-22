import json
import socket
from typing import Dict

HOST = "127.0.0.1"
PORT = 3333
ENCODING = "utf-8"


class NetworkServer(socket.socket):
    def __init__(self, host: str = "127.0.0.2", port: int = 3333):
        self.clients: Dict = {}

        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        print(f"[{'LISTENING':<10}] Bound to the port: {host}:{port}")
        self.bind((host, port))

    def accept_clients(self, amount: int = 4):
        self.listen(4)
        for i in range(amount):
            conn, addr = self.accept()

            name = conn.recv(1024).decode(ENCODING)
            while name in self.clients:
                conn.send(json.dumps({"command": "CONNECTION_REFUSED"}).encode(ENCODING))
                conn.close()
                conn, addr = self.accept()
                name = conn.recv(1024).decode(ENCODING)
            self.clients[name] = {
                "addr": addr,
                "connection": conn
            }
            print(f"[{'CONNECTION':<10}] {name} connected to the Game {i + 1}/{amount} ({addr[0]}:{addr[1]})")
            self.send_to("CONNECTED", name)
        print(self.clients)

    def send_all(self, command: str, **data):
        for name in self.clients:
            jso = {"command": command,
                   "to": name}

            if data:
                for key, value in data:
                    jso[key] = value

            self.clients[name]["connection"].send(json.dumps(jso).encode(ENCODING))

    def send_to(self, command: str, username: str, **data):
        if username not in self.clients:
            return None
        jso = {"command": command,
               "to": username}

        if data:
            for key, value in data.items():
                jso[key] = value

        string_data = json.dumps(jso)

        print(string_data)
        self.clients[username]["connection"].send(string_data.encode(ENCODING))

    def receive(self, name: str):
        if name not in self.clients:
            return None
        return self.clients[name]["connection"].receive().decode(ENCODING)


if __name__ == '__main__':
    server = NetworkServer(host=HOST, port=PORT)
    server.accept_clients()
