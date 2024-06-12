import socket
from prime_generation import generate_prime
def generate_rsa_keys(bits=128):
    p = generate_prime(bits)
    q = generate_prime(bits)
    N = p * q
    phi = (p - 1) * (q - 1)
    E = 65537
    D = pow(E, -1, phi)
    public_key = (E, N)
    private_key = (D, N)
    return public_key, private_key
def encrypt_message(message, public_key):
    rsa_key = public_key
    encrypted_message = pow(message, rsa_key[0], rsa_key[1])
    return encrypted_message
def decrypt_message(encrypted_message, private_key):
    rsa_key = private_key
    decrypted_message = pow(encrypted_message, rsa_key[0], rsa_key[1])
    return decrypted_message
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 12345)
client_socket.connect(server_address)
try:
    public_key, private_key = generate_rsa_keys()
    client_socket.sendall(str(public_key).encode())
    server_public_key = eval(client_socket.recv(4096).decode())
    while True:
        message = input("Enter message: ")
        if message == "BYE":
            encrypted_message = encrypt_message(0, server_public_key)
            client_socket.sendall(str(encrypted_message).encode())
            break
        else:
            encrypted_message = encrypt_message(int.from_bytes(message.encode(), 'big'), server_public_key)
            client_socket.sendall(str(encrypted_message).encode())
finally:
    client_socket.close()