# client.py

import socket
import os
from crypto_utils import (
    generate_aes_key,
    encrypt_file,
    rsa_encrypt
)

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9999
BUFFER_SIZE = 4096

# Load the server's public key
# This file must exist for the client to work.
try:
    with open('server_public.pem', 'rb') as f:
        server_public_key = f.read()
except FileNotFoundError:
    print("[!] Error: 'server_public.pem' not found. Please run the server at least once to generate keys.")
    server_public_key = None # Set to None to handle gracefully if key is missing

def send_file(file_path):
    """
    Sends a specified file to the server after encrypting it with AES,
    and encrypting the AES key with the server's RSA public key.
    It now also sends the original filename to the server.

    Args:
        file_path (str): The path to the file to be sent.
    """
    # Diagnostic print to check what file_path is received
    print(f"[*] client.send_file received path: '{file_path}'")

    if server_public_key is None:
        print("[!] Cannot send file: Server public key is missing.")
        return

    if not os.path.exists(file_path):
        print(f"[!] Error: File not found at '{file_path}'.")
        return

    try:
        with open(file_path, 'rb') as f:
            file_data = f.read()

        # Get the original filename from the file_path
        original_filename = os.path.basename(file_path).encode('utf-8')

        # Generate AES key for symmetric encryption of the file
        aes_key = generate_aes_key()
        # Encrypt the file data using the generated AES key
        encrypted_file = encrypt_file(file_data, aes_key)

        # Encrypt the AES key using the server's RSA public key
        # This ensures only the server (with its private key) can decrypt the AES key
        encrypted_key = rsa_encrypt(aes_key, server_public_key)

        # Establish a socket connection to the server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((SERVER_HOST, SERVER_PORT))
            print(f"[*] Connected to server at {SERVER_HOST}:{SERVER_PORT}.")

            # Send the length of the original filename (4 bytes)
            client_socket.send(len(original_filename).to_bytes(4, 'big'))
            # Send the original filename
            client_socket.send(original_filename)
            print(f"[+] Original filename '{original_filename.decode()}' sent.")

            # Send the length of the encrypted AES key (4 bytes)
            client_socket.send(len(encrypted_key).to_bytes(4, 'big'))
            # Send the encrypted AES key
            client_socket.send(encrypted_key)
            print("[+] Encrypted AES key sent.")

            # Send the length of the encrypted file (8 bytes)
            client_socket.send(len(encrypted_file).to_bytes(8, 'big'))
            # Send the encrypted file data. Use sendall for large files.
            client_socket.sendall(encrypted_file)

            print(f"[+] File '{os.path.basename(file_path)}' and AES key sent successfully.")

    except ConnectionRefusedError:
        print("[!] Error: Connection to server refused. Make sure the server is running and accessible.")
    except Exception as e:
        print(f"[!] An error occurred while sending the file: {e}")

# This block is for testing the client script directly, without the GUI.
# It creates a dummy file if it doesn't exist and attempts to send it.
def start_client_dummy_send():
    dummy_file_path = 'dummy_file_to_send.txt'
    if not os.path.exists(dummy_file_path):
        with open(dummy_file_path, 'w') as f:
            f.write("This is a dummy test file created by client.py for direct execution.\n")
            f.write("It demonstrates the file sending functionality.\n")
    print(f"[*] Attempting to send dummy file: '{dummy_file_path}'")
    send_file(dummy_file_path)

if __name__ == "__main__":
    # If client.py is run directly, it will attempt to send a dummy file.
    # In the GUI, the `send_file` function will be called directly.
    start_client_dummy_send()
