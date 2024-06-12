import socket
from euclide import *
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ("localhost", 12347)
server_socket.bind(server_address)
server_socket.listen(5)
print("Server is listening...")
p = 823
q = 953
n = p * q
Pn = (p - 1) * (q - 1)
key = []
for i in range(2, Pn):
    gcd = euclid(Pn, i)
    if gcd == 1:
        key.append(i)
e = 313
r, d = exteuclid(Pn, e)
if r == 1:
    d = int(d)
    print("Decryption key is:", d)
else:
    print("Multiplicative inverse for the given encryption key does not exist.")
connection, client_address = server_socket.accept()
print("Client connected:", client_address)
try:
    while True:
        data = connection.recv(1024).decode()
        if not data:
            break
        print("Received from client:", data)
        M1 = int(data)
        M = (M1 ** e) % n
        print("Decrypted message from client:", M)
        if M == M1:
            print("Authentication successful. Message accepted.")
            connection.sendall("Message accepted".encode())
        else:
            print("Authentication failed. Message rejected.")
            connection.sendall("Message rejected".encode())
finally:
    connection.close()
