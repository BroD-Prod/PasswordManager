from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

class Manager_Password:
    def __init__(self):
        pass

    def encrypt_site_password(self, password):
        key = get_random_bytes(32)
        iv = get_random_bytes(32)
        cipher = AES.new(key=key,mode=AES.MODE_CBC,iv=iv)
        ciphertext = cipher.encrypt(pad(password,16))
        return ciphertext