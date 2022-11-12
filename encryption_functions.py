from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


def generate_key():
    # Generating a key to encrypt and decrypt passwords
    return Fernet.generate_key()


def get_hash(string):
    # Hashing a string (Used to hash the master password)
    byte_string = string.encode()

    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(byte_string)

    hashed_string = digest.finalize()

    return hashed_string


def encrypt_password(key, password):
    # Encrypt a given password from the user 
    fernet = Fernet(key)

    encrypted_password = fernet.encrypt(password.encode())

    return encrypted_password


def decrypt_password(key, password):
    # Decrypt an encrypted password from the database
    fernet = Fernet(key)

    decrypted_password = (fernet.decrypt(password.encode())).decode()

    return decrypted_password
