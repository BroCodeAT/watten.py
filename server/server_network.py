import json
import socket
import multiprocessing
from typing import Dict
from server.models import ClientData


class NetworkServer:
    def __init__(self, host: str = "127.0.0.2", port: int = 3333):
        self.clients: dict[str, ClientData] = {}
        self.ENCODING = "utf-8"
        self.conn: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.que: multiprocessing.Queue = multiprocessing.Queue()
        self.listeners: list[multiprocessing.Process] = []

        print(f"[{'LISTENING':<10}] Bound to the port: {host}:{port}")
        self.conn.bind((host, port))

    def accept_clients(self, amount: int = 4):
        self.conn.listen(4)
        for i in range(amount):
            conn, addr = self.conn.accept()

            name = conn.recv(1024).decode(self.ENCODING)
            while name in self.clients:
                conn.send(json.dumps({"command": "CONNECTION_REFUSED"}).encode(self.ENCODING))
                conn.close()
                conn, addr = self.con.accept()
                name = conn.recv(1024).decode(self.ENCODING)
            self.clients[name] = {ClientData.new_conn(name, conn, addr)}
            print(f"[{'CONNECTION':<10}] {name} connected to the Game {i + 1}/{amount} ({addr[0]}:{addr[1]})")
            self.send_to("CONNECTED", name)

    def send_all(self, command: str, **data):
        for name in self.clients:
            jso = {"command": command,
                   "to": name}

            if data:
                for key, value in data:
                    jso[key] = value

            self.clients[name].conn.send(json.dumps(jso).encode(self.ENCODING))

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
        self.clients[username].conn.send(string_data.encode(self.ENCODING))

    def receive(self, name: str):
        if name not in self.clients:
            return None

        return self.clients[name].conn.recv(1024).decode(self.ENCODING)

    def receive_from_client(self, client):
        data = self.receive(client)
        try:
            return json.loads(data)
        except json.decoder.JSONDecodeError:
            commands = []
            commands_len = data.count("command")
            # Remove first and last {,} to be sure to add the {,} afterwards in the for loop
            partial_commands = data[1:-1].split("}{")
            if len(partial_commands) == commands_len:
                for command in partial_commands:
                    # Add the {, } to the command again to make sure it is json loadable
                    commands.append(json.loads("{" + command + "}"))
            return commands

    def allow_responses_from(self, *clients: str):
        for client in clients:
            self.listeners.append(multiprocessing.Process(target=self.wait_for_response, args=(client,)))
            self.listeners[-1].run()

    def stop_responses(self):
        for listener in self.listeners:
            listener.close()
        self.listeners = []

    def wait_for_response(self, client: str):
        while True:
            recv = self.receive_from_client(client)
            if recv:
                if isinstance(recv, list):
                    for com in recv:
                        self.que.put(com)
                    return
                self.que.put(recv)


if __name__ == '__main__':
    HOST = "127.0.0.1"
    PORT = 3333
    server = NetworkServer(host=HOST, port=PORT)
    server.accept_clients()
