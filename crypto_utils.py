from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import os

AES_KEY_SIZE = 32  # 256 bits
BLOCK_SIZE = AES.block_size


def pad(data):
    padding_len = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return data + bytes([padding_len] * padding_len)


def unpad(data):
    padding_len = data[-1]
    return data[:-padding_len]


def generate_aes_key():
    return get_random_bytes(AES_KEY_SIZE)


def encrypt_file(file_input, aes_key):
    """
    Encrypt file data using AES-CBC.
    Accepts either a file path (str) or raw bytes.
    Returns: IV + encrypted data
    """
    cipher = AES.new(aes_key, AES.MODE_CBC)
    
    if isinstance(file_input, str):
        with open(file_input, 'rb') as f:
            data = pad(f.read())
    elif isinstance(file_input, bytes):
        data = pad(file_input)
    else:
        raise TypeError("file_input must be a file path (str) or file content (bytes)")
    
    encrypted = cipher.encrypt(data)
    return cipher.iv + encrypted


def decrypt_file(encrypted_data, aes_key):
    iv = encrypted_data[:BLOCK_SIZE]
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(encrypted_data[BLOCK_SIZE:]))


def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key


def rsa_encrypt(data, public_key_bytes):
    public_key = RSA.import_key(public_key_bytes)
    cipher_rsa = PKCS1_OAEP.new(public_key)
    return cipher_rsa.encrypt(data)


def rsa_decrypt(encrypted_data, private_key_bytes):
    private_key = RSA.import_key(private_key_bytes)
    cipher_rsa = PKCS1_OAEP.new(private_key)
    return cipher_rsa.decrypt(encrypted_data)
