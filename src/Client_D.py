import socket
import pickle as p
import enum

# Data is a class that contains the user command, name of the file, and the contents of that file
class Data:
    command = 0
    fileName = ""
    fileData = ""

# Command is an enum which represents user commands as an int
class Command(enum.Enum):
    HELP = 0
    UPLOAD = 1
    DELETE = 2
    SYNC = 3

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

print("Connected to " + str(socket.gethostname()))
Response = ClientSocket.recv(1024)
while True:
    d = Data()
    d.command = Command[input("Enter command: ").upper()].value
    d.fileName = "README.md"
    # d.fileName = input("Enter file name: ")
    ds = p.dumps(d)
    ClientSocket.send(ds)
    Response = ClientSocket.recv(1024)
    print(Response.decode('utf-8'))

ClientSocket.close()