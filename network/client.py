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

    def server_connect(self, name: str, host: str = "127.0.0.2", port: int = 3333) -> bool:
        self.server.connect((host, port))
        with self.lock:
            self.server.send(name.encode())
        resp = self.recv_from_server()
        if resp.get("command") == "CONNECTED":
            if resp.get("name") == name:
                self.listener.start()
                return True
        elif resp.get("command") == "CONNECTION_REFUSED":
            self.server.close()
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            return False

    def send_to_server(self, msg: str):
        to_send = msg.encode(FORMAT)
        with self.lock:
            self.server.send(to_send)

    def recv_from_server(self):
        data = self.server.recv(1024).decode()
        print(data)
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

    def recv_in_process(self):
        while self.running:
            recv = self.recv_from_server()
            print(recv)
            if recv:
                if isinstance(recv, list):
                    for com in recv:
                        self.que.put(com)
                    return
                self.que.put(recv)
