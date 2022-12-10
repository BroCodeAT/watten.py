import socket

HOST = "127.0.0.1"
PORT = 3333
FORMAT = "UTF-8"

class NetworkClient(socket.socket):
    def __init__(self):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)

    def server_connect(self, name: str, host: str = "127.0.0.1", port: int = 3333):
        self.connect((host, port))
        self.send(name.encode())

    def send(self,msg: str):
        to_send = msg.encode(FORMAT)
        self.send(to_send)



if __name__ == '__main__':
    client = NetworkClient()
    username = input("Please enter your name: ")
    client.server_connect(username, host=HOST, port=PORT)
    
    client.send("test 1234")