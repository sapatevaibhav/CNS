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
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 12345)
server_socket.bind(server_address)
server_socket.listen(1)
print("Server is listening...")
while True:
    connection, client_address = server_socket.accept()
    try:
        print("Client is connected at:", client_address)
        server_public_key, server_private_key = generate_rsa_keys()
        connection.sendall(str(server_public_key).encode())
        client_public_key = eval(connection.recv(4096).decode())
        while True:
            encrypted_message = connection.recv(4096)
            decrypted_message = decrypt_message(int(encrypted_message.decode()), server_private_key)
            if decrypted_message == 0:
                print("Received termination message! Exiting...")
                break
            print("Received:", decrypted_message.to_bytes((decrypted_message.bit_length() + 7) // 8, 'big').decode())
        connection.close()
        break
    finally:
        connection.close()