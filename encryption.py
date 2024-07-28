from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes


def encrypt_pwd(password: str, key: bytes) -> tuple[bytes, bytes, bytes]:
    """
    Encrypts a password using AES encryption with the EAX mode.

    Args:
        password (str): The password to be encrypted.
        key (bytes): The AES encryption key.

    Returns:
        tuple: A tuple containing the ciphertext, nonce, and tag.
            - ciphertext (bytes): The encrypted password.
            - nonce (bytes): The nonce used for encryption.
            - tag (bytes): The tag used for authentication.

    Raises:
        TypeError: If the password is not a string or the key is not bytes.
    """
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(password.encode("utf8"))
    return ciphertext, cipher.nonce, tag


def decrypt_pwd(ciphertext: bytes, nonce: bytes, tag: bytes, key: bytes) -> str:
    """
    Decrypts a password using AES encryption with the EAX mode.

    Args:
        ciphertext (bytes): The encrypted password.
        nonce (bytes): The nonce used for encryption.
        tag (bytes): The tag used for authentication.
        key (bytes): The AES encryption key.

    Returns:
        str: The decrypted password.
    """
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    password = cipher.decrypt_and_verify(ciphertext, tag)
    return password.decode("utf8")


def add_data(ciphertext: bytes, nonce: bytes, tag: bytes) -> bytes:
    """
    Concatenates the ciphertext, nonce, and tag into a single bytes object.
    Args:
        ciphertext (bytes): The encrypted data.
        nonce (bytes): The nonce used for encryption.
        tag (bytes): The tag used for authentication.
    Returns:
        bytes: The concatenated bytes object containing the ciphertext, nonce, and tag.
    """
    return ciphertext + nonce + tag


def separate_data(data: bytes, nonce_len: int, tag_len: int) -> tuple[bytes, bytes, bytes]:
    """
    Separates the given data into ciphertext, nonce, and tag.
    Args:
        data (bytes): The data to be separated.
        nonce_len (int): The length of the nonce.
        tag_len (int): The length of the tag.
    Returns:
        tuple[bytes, bytes, bytes]: A tuple containing the ciphertext, nonce, and tag.
    """
    data_len = len(data)
    tag_start = data_len - tag_len
    nonce_start = tag_start - nonce_len
    ciphertext = data[:nonce_start]
    nonce = data[nonce_start:tag_start]
    tag = data[tag_start:]
    return ciphertext, nonce, tag


# Testing
""" key = get_random_bytes(16)
password = "password"
encrypted_password, nonce, tag = encrypt_pwd(password, key)
decrypted_password = decrypt_pwd(encrypted_password, nonce, tag, key)
print(encrypted_password)
print(type(encrypted_password))
print(nonce)
print(type(nonce))
print(tag)
print(type(tag))
print(decrypted_password)
print(type(decrypted_password)) """
