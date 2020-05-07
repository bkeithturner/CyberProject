'''# Imports
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from binascii import hexlify
import socket
import os
from _thread import *

# The message to be encrypted
message = b'Public and Private keys encryption at server'

# Generating private key (RsaKey object) of key length of 1024 bits
server_private_key = RSA.generate(1024)

# Generating the public key (RsaKey object) from the private key
server_public_key = server_private_key.publickey()
print(type(server_private_key), type(server_public_key))

# Converting the RsaKey objects to string
server_private_pem = server_private_key.export_key().decode()
server_public_pem = server_public_key.export_key().decode()
print(type(server_private_pem), type(server_public_pem))

# Writing down the private and public keys to 'pem' files
with open('server_private_pem.pem', 'w') as pr:
    pr.write(server_private_pem)
with open('server_public_pem.pem', 'w') as pu:
    pu.write(server_public_pem)

# Importing keys from files, converting it into the RsaKey object
pr_key = RSA.import_key(open('server_private_pem.pem', 'r').read())
pu_key = RSA.import_key(open('server_public_pem.pem', 'r').read())
print(type(pr_key), type(pu_key))

# Instantiating PKCS1_OAEP object with the public key for encryption
cipher = PKCS1_OAEP.new(key=pu_key)

# Encrypting the message with the PKCS1_OAEP object
cipher_text = cipher.encrypt(message)
print(cipher_text)

# Instantiating PKCS1_OAEP object with the private key for decryption
decrypt = PKCS1_OAEP.new(key=pr_key)

# Decrypting the message with the PKCS1_OAEP object
decrypted_message = decrypt.decrypt(cipher_text)
print(decrypted_message)'''

'''
# Converting the RsaKey objects to string
private_pem = private_key.export_key().decode()
public_pem = public_key.export_key().decode()
print(type(private_pem), type(public_pem))
print(private_pem)
print(public_pem)
'''
import os
import socket
import pickle as p
import enum
from _thread import *

reply = ""

# Data is a class that contains the user command, name of the file, and the contents of that file
class Data:
    def __init__(self, command, fileName, fileData):
        self.command = command
        self.fileName = fileName
        self.fileData = fileData

# Command is an enum which represents user commands as an int
class Command(enum.Enum):
    HELP = 0
    UPLOAD = 1
    DELETE = 2
    SHARE = 3

#TODO: Upload file to database
def upload(data):
    global reply
    p.dump(data.fileData, open('Storage/' + data.fileName, 'wb'))
    with open('Storage/' + data.fileName, 'wb') as f:
        f.write(data.fileData)
    reply = "Uploading " + data.fileName

#TODO: Delete file from database
def delete(data):
    global reply
    try:
        os.remove('Storage/' + data.fileName)
        reply = "Deleting " + data.fileName
    except:
        reply = data.fileName + " doesn't exist"

#TODO: sync files
def sync(data):
    global reply
    data.fileData = p.load(open('Storage/' + data.fileName, 'rb'))
    reply = "Syncing " + data.fileName

#TODO: Share database file with another user
def share(data):
    global reply
    reply = "Syncing " + data.fileName

# Set up socket
ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233
ThreadCount = 0
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection..')
ServerSocket.listen(5)

def threaded_client(connection):
    global reply

    connection.send(str.encode('Welcome to the Server\n'))
    while True:
        data = p.loads(connection.recv(2048))
        cmd = Command(data.command).name
        fname = data.fileName

        if cmd == "UPLOAD":
            upload(data)
        elif cmd == "DELETE":
            delete(data)
        elif cmd == "HELP":
            reply = "Figure it out yourself!"
        else:
            reply = 'Server Says: ' + fname
        if not cmd:
            break
        connection.sendall(str.encode(reply))
    connection.close()

while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client,))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()

