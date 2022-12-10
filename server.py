import socket

SERVER = "127.0.0.1"
PORT = 12345

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("socket created")

    s.bind((SERVER, PORT)) 
    print("socket connecting this port: {} ".format(PORT))

    s.listen(4)      
    print("socket listening")

except socket.error as msg:
    print("err :",msg)


while True:
    conn, addr = s.accept()

