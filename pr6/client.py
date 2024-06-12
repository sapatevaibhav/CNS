import socket
from euclide import *
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ("localhost", 12347)
client_socket.connect(server_address)
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
try:
    while True:
        message = input("Enter message ('bye' to exit): ")
        if message == "bye":
            break
        M = int(message)
        S = (M ** d) % n
        client_socket.sendall(str(S).encode())
        response = client_socket.recv(1024).decode()
        print("Server response:", response)
finally:
    client_socket.close()