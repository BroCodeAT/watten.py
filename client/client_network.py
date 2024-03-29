import time
import json
import socket
import multiprocessing

from typing import Any


class NetworkClient:
    """
    A class to handle the network part of the client

    ...

    Constants
    ---------
    ENCODING : str -> "utf-8"
        The encoding when sending/receiving data

    Attributes
    ----------
    lock : multiprocessing.Lock
        A lock to lock the socket connection when receiving data
    que : multiprocessing.Queue
        A queue to store the commands received from the client
    server : socket.socket
        The connection to the server
    listener : multiprocessing.Process
        A process to listen to commands from the server
    running : bool
        If the process should run

    Methods
    -------
    send(data: bytes) -> None
        Send data to the server (first length then data)
    recv() -> bytes
        Function to receive the exact amount of bytes
    server_connect(self, name: str, host: str = "127.0.0.2", port: int = 3333) -> bool
        Connect to the server with a given name
    send_to_server(self, command: str, username: str, **data) -> None
        Send a command to the server
    recv_from_server(self) -> dict | list[dict]
        Receive data from the server and convert it to a command
    recv_in_process(self) -> None
        The method the listener will listen to, to receive data from the server
    """
    def __init__(self):
        """
        Initialize a new NetworkClient
        Setup needed attributes
        """
        self.ENCODING = "utf-8"
        self.que = multiprocessing.Queue()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener = multiprocessing.Process(target=self.recv_in_process, daemon=True)
        self.running: bool = True

    def send(self, data: bytes):
        """
        Send data to the server (first length then data)

        Parameters
        ----------
        data : bytes
            The data to send to the server

        Returns
        -------
        None
        """
        length = len(data)
        byte_length = length.to_bytes(16, "big")
        self.server.send(byte_length)
        self.server.send(data)

    def recv(self) -> bytes:
        """
        Function to receive the exact amount of bytes
        First the length will be received than the client receives the data

        Returns
        -------
        bytes : The data received
        """
        length = int.from_bytes(self.server.recv(16), "big")
        data = self.server.recv(length)
        return data

    def server_connect(self, name: str, pwd: str, host: str = "127.0.0.2", port: int = 3333) -> bool:
        """
        Connect to the server with a given name

        Parameters
        ----------
        name : str
            The name of the client that wants to connect to the server
        host : str (default: 127.0.0.2)
            The IPv4-Address of the Server to connect to
        port : int (default: 3333)
            The Port of the Server to connect to

        Returns
        -------

        """
        self.server.connect((host, port))
        login_credentials  = json.dumps({"user": name, "password": pwd})
    
        self.send(login_credentials.encode())
        resp = self.recv_from_server()
        if resp.get("command") == "CONNECTED":
            if resp.get("to") == name:
                print("listener_started")
                self.listener.start()
                return True
        elif resp.get("command") == "CONNECTION_REFUSED":
            self.server.close()
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            return False

    def send_to_server(self, command: str, username: str, **data: Any) -> None:
        """
        Send a command to the server

        Parameters
        ----------
        command : str
            The command name the server should receive
        username : str
            The name of the client that send the command
        data : dict
            Additional data the server needs to process the command

        Returns
        -------
        None
        """
        jso = {"command": command,
               "from": username}

        if data:
            for key, value in data.items():
                jso[key] = value

        string_data = json.dumps(jso)
        print(f"[{'SENDING':<10}] {string_data}")

        self.send(string_data.encode(self.ENCODING))

    def recv_from_server(self) -> dict | list[dict]:
        """
        Receive data from the server and convert it to a command
        (Multiple commands can be received at once)

        Returns
        -------
        dict : a command received from the server
        list[dict] : a list of commands received from the server
        """
        data = self.recv().decode()
        print(f"[{'RECEIVED':<10}] {data}")
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

    def recv_in_process(self) -> None:
        """
        The method the listener will listen to, to receive data from the server
        When a command is received it will be added to the queue

        Returns
        -------
        None
        """
        while self.running:
            recv = self.recv_from_server()
            if recv:
                if isinstance(recv, list):
                    for com in recv:
                        self.que.put(com)
                    return
                self.que.put(recv)
            time.sleep(0.2)
