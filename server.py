# server.py

import socket
import os
import threading # Import threading for the server_running flag

from crypto_utils import (
    generate_rsa_keys,
    rsa_decrypt,
    decrypt_file
)

HOST = '0.0.0.0'
PORT = 9999
BUFFER_SIZE = 4096

# RSA Key file paths
PRIVATE_KEY_FILE = 'server_private.pem'
PUBLIC_KEY_FILE = 'server_public.pem'

# Global flag to control server execution
server_running = False
server_socket_instance = None # To hold the socket object for closing

# Generate RSA keys if not present
if not os.path.exists(PRIVATE_KEY_FILE) or not os.path.exists(PUBLIC_KEY_FILE):
    private_key, public_key = generate_rsa_keys()
    with open(PRIVATE_KEY_FILE, 'wb') as f:
        f.write(private_key)
    with open(PUBLIC_KEY_FILE, 'wb') as f:
        f.write(public_key)
else:
    with open(PRIVATE_KEY_FILE, 'rb') as f:
        private_key = f.read()

def start_server(save_directory=None):
    """
    Starts the server to listen for incoming file transfers.
    It generates RSA keys if they don't exist, receives an encrypted AES key,
    decrypts it, receives the encrypted file, decrypts it, and saves it.

    Args:
        save_directory (str, optional): The directory where received files will be saved.
                                        If None, files will be saved in a 'received_files'
                                        subdirectory in the current working directory.
    """
    global server_running, server_socket_instance, private_key
    if server_running:
        print("[!] Server is already running.")
        return

    server_running = True
    print(f"[+] Starting server on {HOST}:{PORT}...")

    try:
        server_socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket_instance.settimeout(1) # Set a timeout to allow checking the flag
        server_socket_instance.bind((HOST, PORT))
        server_socket_instance.listen(1) # Listen for one connection at a time
        print(f"[+] Server listening on {HOST}:{PORT}...")

        while server_running:
            try:
                conn, addr = server_socket_instance.accept()
                with conn:
                    print(f"[+] Connected by {addr}")

                    # New Step: Receive filename length (4 bytes) and the actual filename
                    filename_length = int.from_bytes(conn.recv(4), 'big')
                    original_filename = conn.recv(filename_length).decode('utf-8')
                    print(f"[+] Receiving file: '{original_filename}'")

                    # Determine the full path where the file will be saved
                    if save_directory:
                        os.makedirs(save_directory, exist_ok=True)
                        save_path = os.path.join(save_directory, original_filename)
                    else:
                        default_save_dir = "received_files"
                        os.makedirs(default_save_dir, exist_ok=True)
                        save_path = os.path.join(default_save_dir, original_filename)

                    # Step 1: Receive encrypted AES key size (4 bytes) and data
                    encrypted_key_size = int.from_bytes(conn.recv(4), 'big')
                    encrypted_aes_key = conn.recv(encrypted_key_size)

                    # Step 2: Decrypt AES key using the server's private RSA key
                    aes_key = rsa_decrypt(encrypted_aes_key, private_key)
                    print("[+] AES key received and decrypted.")

                    # Step 3: Receive encrypted file size (8 bytes) and the file data
                    file_size = int.from_bytes(conn.recv(8), 'big')
                    received_data = b''
                    while len(received_data) < file_size:
                        chunk = conn.recv(min(BUFFER_SIZE, file_size - len(received_data)))
                        if not chunk:
                            break
                        received_data += chunk
                    print(f"[+] Encrypted file received: {len(received_data)} bytes")

                    # Step 4: Decrypt the received file data using the decrypted AES key
                    decrypted_file_data = decrypt_file(received_data, aes_key)
                    with open(save_path, 'wb') as f:
                        f.write(decrypted_file_data)
                    print(f"[+] File decrypted and saved as '{save_path}'")

            except socket.timeout:
                # Timeout occurred, check server_running flag and continue loop
                pass
            except Exception as e:
                print(f"[!] Error during file transfer: {e}")
                if server_running: # Only print if server is still supposed to be running
                    print("[!] Server encountered an error, but will continue listening.")
        print("[+] Server stopped listening.")
    except Exception as e:
        print(f"[!] Server startup error: {e}")
    finally:
        if server_socket_instance:
            server_socket_instance.close()
            print("[+] Server socket closed.")
        server_running = False # Ensure flag is reset

def stop_server():
    """Sets the global flag to stop the server's listening loop."""
    global server_running, server_socket_instance
    if server_running:
        print("[*] Stopping server...")
        server_running = False
        # The start_server function's loop will exit due to the flag and timeout,
        # and its finally block will close the socket.
    else:
        print("[!] Server is not running.")

if __name__ == '__main__':
    start_server()
