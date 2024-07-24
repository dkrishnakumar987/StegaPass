from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes

def encrypt_pwd(password, key):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(password.encode('utf8'))
    return ciphertext, cipher.nonce, tag

def decrypt_pwd(ciphertext, nonce, tag, key):
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    password = cipher.decrypt_and_verify(ciphertext, tag)
    return password

""" Testing
key = get_random_bytes(16)
password = "password"
encrypted_password, nonce, tag = encrypt_pwd(password, key)
decrypted_password = decrypt_pwd(encrypted_password, nonce, tag, key)
print (encrypted_password)
print(type(encrypted_password))
print(nonce)
print(type(nonce))
print(tag)
print(type(tag))
print(decrypted_password)
print(type(decrypted_password)) """