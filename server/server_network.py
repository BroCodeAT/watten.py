import json
import socket
import multiprocessing
from typing import Dict, Any
from models import ClientData
from database import Database


class NetworkServer:
    """
    A class to handle the network part of the server

    ...

    Constants
    ---------
    ENCODING : str -> "utf-8"
        The encoding when sending/receiving data

    Attributes
    ----------
    clients : dict[str, ClientData] (default: {})
        A dictionary of every Client
    conn : socket.socket
        A TCP/IPv4 connection to allow clients to connect to the server
    que : multiprocessing.Queue
        A que to receive multiple commands at once
    listeners : list[multiprocessing.Process] (default: [])
        A list of processes to receive data simultaneously

    Methods
    -------
    send(conn: socket.socket, data: bytes) -> None
        Send data to the client (first length then data)
    recv(conn: socket.socket) -> bytes
        Function to receive the exact amount of bytes
    accept_clients(amount: int = 4) -> None
        Allow 'amount' clients to connect to the Server
    send_all(command: str, **data) -> None
        Send a command to every client in self.clients
    send_to(command: str, username: str, **data) -> None
        Send data to a Client
    receive(name: str) -> str | None
        Receive data from a client
    receive_from_client(client) -> list[dict] | dict
        Listen to ONE response of a client
    allow_responses_from(*clients: str) -> None
        Start processes for every given client and listen if they are sending commands
    stop_responses() -> None
        Close all running listeners
    wait_for_response(client: str) -> None
        Wait for Responses from a client
    """
    def __init__(self, db:Database, host: str = "127.0.0.2", port: int = 3333):
        """
        Initialize a new NetworkServer to handle the network

        Parameters
        ----------
        host : str
            The IP-Address the server will be bind to
        port : int
            The Port the server will be bind to
        """
        self.db = db
        self.clients: dict[str, ClientData] = {}
        self.ENCODING = "utf-8"
        self.conn: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.que: multiprocessing.Queue = multiprocessing.Queue()
        self.listeners: list[multiprocessing.Process] = []

        print(f"[{'LISTENING':<10}] Bound to the port: {host}:{port}")
        self.conn.bind((host, port))

    def send(self, conn: socket.socket, data: bytes) -> None:
        """
        Send data to the client (first length then data)

        Parameters
        ----------
        conn : socket.socket
            The connection to the client
        data : bytes
            The data to send to the client

        Returns
        -------
        None
        """
        length = len(data)
        conn.send(length.to_bytes(16, "big"))
        conn.send(data)

    def recv(self, conn: socket.socket) -> bytes:
        """
        Function to receive the exact amount of bytes
        First the length will be received than the client receives the data

        Parameters
        ----------
        conn : socket.socket
            The connection to the client

        Returns
        -------
        bytes : The data received
        """
        byte_length = conn.recv(16)
        length = int.from_bytes(byte_length, "big")
        data = conn.recv(length)
        return data

    def accept_clients(self, amount: int = 4) -> None:
        """
        Allow 'amount' clients to connect to the Server

        Receive the name and store them as a ClientData

        Parameters
        ----------
        amount : int
            How many clients are able to connect

        Returns
        -------
        None
        """
        self.conn.listen(4)

        while len(self.clients) < amount:
            name = ""
            conn, addr = self.conn.accept()

            login_crerdentials: dict = json.loads(self.recv(conn).decode(self.ENCODING))
            name = login_crerdentials.get("user")

            if name in self.clients:
                self.send(conn, json.dumps({"command": "CONNECTION_REFUSED"}).encode(self.ENCODING))
                conn.close()
            
            #checking if the user exists and if the password is correct
            elif self.db.verify_user(name, login_crerdentials.get("password")):
                self.clients[name] = ClientData.new_conn(name, conn, addr)
                print(f"[{'CONNECTION':<10}] {name} connected to the Game {len(self.clients)}/{amount} ({addr[0]}:{addr[1]})")
                self.send_to("CONNECTED", name)
            else:
                self.send(conn, json.dumps({"command": "CONNECTION_REFUSED"}).encode(self.ENCODING))
                conn.close()

    def send_all(self, command: str, **data: Any) -> None:
        """
        Send a command to every client in self.clients

        Parameters
        ----------
        command : str
            The command every client should receive
        data : any
            Additional data every client should receive

        Returns
        -------
        None
        """
        for name in self.clients:
            self.send_to(command, name, **data)

    def send_to(self, command: str, username: str, **data: Any) -> None:
        """
        Send data to a Client

        Parameters
        ----------
        command : str
            The command the Client should receive
        username : str
            The username the command should be sent to
        data : any
            Additional data the client needs
        Returns
        -------
        None
        """
        if username not in self.clients:
            return None
        jso = {"command": command,
               "to": username}

        if data:
            for key, value in data.items():
                jso[key] = value

        string_data = json.dumps(jso)
        print(f"[{'SENDING':<10}] {string_data}")

        self.send(self.clients[username].conn, string_data.encode(self.ENCODING))

    def receive(self, name: str) -> str | None:
        """
        Receive data from a client

        Parameters
        ----------
        name : The name of the client to receive the data from

        Returns
        -------
        str : The response
        None : The name of the client is not given in self.clients
        """
        if name not in self.clients:
            return None

        return self.recv(self.clients[name].conn).decode(self.ENCODING)

    def receive_from_client(self, client) -> list[dict] | dict:
        """
        Listen to ONE response of a client
        (sometimes can be more command than one)

        Parameters
        ----------
        client: str
            The client to receive the command(s) from

        Returns
        -------
        dict : One Command
        list[dict] : Multiple Commands
        """
        data = self.receive(client)
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

    def allow_responses_from(self, *clients: str) -> None:
        """
        Start processes for every given client and listen if they are sending commands

        Parameters
        ----------
        clients : list[str]
            A list of clients to listen to

        Returns
        -------
        None
        """
        for client in clients:
            self.listeners.append(multiprocessing.Process(target=self.wait_for_response, args=(client,)))
            self.listeners[-1].run()

    def stop_responses(self) -> None:
        """
        Close all running listeners
        (Stop waiting for commands from clients)

        Returns
        -------
        None
        """
        for listener in self.listeners:
            listener.close()
        self.listeners = []

    def wait_for_response(self, client: str) -> None:
        """
        Wait for Responses from a client
        (used as a method in a process to receive multiple commands at once)

        Parameters
        ----------
        client : str
            The name of the client to receive data from

        Returns
        -------
        None
        """
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
