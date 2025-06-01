# Icrypto_utils.py

from abc import ABC, abstractmethod

class ICryptoUtils(ABC):
    """
    Abstract Base Class (ABC) defining the interface for cryptographic utilities.
    Any class implementing this interface must provide concrete
    implementations for the defined abstract methods.
    """

    @abstractmethod
    def pad(self, data: bytes) -> bytes:
        """
        Pads the input data to be a multiple of the AES block size.

        Args:
            data (bytes): The raw data to be padded.

        Returns:
            bytes: The padded data.
        """
        pass

    @abstractmethod
    def unpad(self, data: bytes) -> bytes:
        """
        Removes padding from the decrypted data.

        Args:
            data (bytes): The padded data.

        Returns:
            bytes: The unpadded data.
        """
        pass

    @abstractmethod
    def generate_aes_key(self) -> bytes:
        """
        Generates a random AES key of a predefined size (256 bits).

        Returns:
            bytes: The generated AES key.
        """
        pass

    @abstractmethod
    def encrypt_file(self, file_input: bytes, aes_key: bytes) -> bytes:
        """
        Encrypts file data using AES-CBC mode.

        Args:
            file_input (bytes): The raw file content to be encrypted.
            aes_key (bytes): The AES key for encryption.

        Returns:
            bytes: The Initialization Vector (IV) concatenated with the encrypted data.
        """
        pass

    @abstractmethod
    def decrypt_file(self, encrypted_data: bytes, aes_key: bytes) -> bytes:
        """
        Decrypts AES-CBC encrypted data.

        Args:
            encrypted_data (bytes): The IV concatenated with the encrypted data.
            aes_key (bytes): The AES key for decryption.

        Returns:
            bytes: The original decrypted and unpadded data.
        """
        pass

    @abstractmethod
    def generate_rsa_keys(self) -> tuple[bytes, bytes]:
        """
        Generates a new RSA key pair (private and public keys).

        Returns:
            tuple[bytes, bytes]: A tuple containing the private key bytes and the public key bytes.
        """
        pass

    @abstractmethod
    def rsa_encrypt(self, data: bytes, public_key_bytes: bytes) -> bytes:
        """
        Encrypts data using RSA public key encryption (PKCS1_OAEP).

        Args:
            data (bytes): The data to be encrypted.
            public_key_bytes (bytes): The RSA public key in bytes.

        Returns:
            bytes: The RSA encrypted data.
        """
        pass

    @abstractmethod
    def rsa_decrypt(self, encrypted_data: bytes, private_key_bytes: bytes) -> bytes:
        """
        Decrypts data using RSA private key decryption (PKCS1_OAEP).

        Args:
            encrypted_data (bytes): The RSA encrypted data.
            private_key_bytes (bytes): The RSA private key in bytes.

        Returns:
            bytes: The decrypted data.
        """
        pass

