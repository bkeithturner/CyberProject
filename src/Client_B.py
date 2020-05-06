# Imports
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from binascii import hexlify
import socket

# The message to be encrypted
message = b'Public and Private keys encryption Client B'

# Generating private key (RsaKey object) of key length of 1024 bits
client_b_private_key = RSA.generate(1024)

# Generating the public key (RsaKey object) from the private key
client_b_public_key = client_b_private_key.publickey()
print(type(client_b_private_key), type(client_b_public_key))

# Converting the RsaKey objects to string
client_b_private_pem = client_b_private_key.export_key().decode()
client_b_public_pem = client_b_public_key.export_key().decode()
print(type(client_b_private_pem), type(client_b_public_pem))

# Writing down the private and public keys to 'pem' files
with open('client_b_private_pem.pem', 'w') as b_pr:
    b_pr.write(client_b_private_pem)
with open('client_b_public_pem.pem', 'w') as b_pu:
    b_pu.write(client_b_public_pem)

# Importing keys from files, converting it into the RsaKey object
b_pr_key = RSA.import_key(open('client_b_private_pem.pem', 'r').read())
b_pu_key = RSA.import_key(open('client_b_public_pem.pem', 'r').read())
print(type(b_pr_key), type(b_pu_key))

# Instantiating PKCS1_OAEP object with the public key for encryption
cipher = PKCS1_OAEP.new(key=b_pu_key)

# Encrypting the message with the PKCS1_OAEP object
cipher_text = cipher.encrypt(message)
print(cipher_text)

# Instantiating PKCS1_OAEP object with the private key for decryption
decrypt = PKCS1_OAEP.new(key=b_pr_key)

# Decrypting the message with the PKCS1_OAEP object
decrypted_message = decrypt.decrypt(cipher_text)
print(decrypted_message)

# Converting the RsaKey objects to string
client_b_private_pem = client_b_private_key.export_key().decode()
client_b_public_pem = client_b_public_key.export_key().decode()
print(type(client_b_private_pem), type(client_b_public_pem))
print(client_b_private_pem)
print(client_b_public_pem)

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

Response = ClientSocket.recv(1024)
while True:
    Input = input('Say Something: ')
    ClientSocket.send(str.encode(Input))
    Response = ClientSocket.recv(1024)
    print(Response.decode('utf-8'))

ClientSocket.close()
