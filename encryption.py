from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes

def encrypt_pwd(password,key):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(password.encode('utf8'))
    return ciphertext, cipher.nonce, tag
