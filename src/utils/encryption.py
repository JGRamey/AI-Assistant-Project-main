"""Handles encryption and decryption of sensitive data."""
import os
from cryptography.fernet import Fernet

def load_encryption_key():
    """Loads the encryption key from an environment variable or creates one."""
    key = os.environ.get("ENCRYPTION_KEY")
    if not key:
        key = Fernet.generate_key().decode()
        os.environ["ENCRYPTION_KEY"] = key
    return key.encode()


def encrypt_data(data: str) -> str:
    """Encrypts data using Fernet symmetric encryption."""
    f = Fernet(load_encryption_key())
    encrypted_data = f.encrypt(data.encode())
    return encrypted_data.decode()


def decrypt_data(encrypted_data: str) -> str:
    """Decrypts data using Fernet symmetric encryption."""
    f = Fernet(load_encryption_key())
    decrypted_data = f.decrypt(encrypted_data.encode())
    return decrypted_data.decode()
