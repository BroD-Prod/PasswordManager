from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

class Manager_Password:
    def __init__(self):
        pass

    def encrypt_site_password(self, password):
        cipher = AES.new(key=get_random_bytes(32),mode=AES.MODE_CBC,iv=get_random_bytes(32))
        ciphertext = cipher.encrypt(pad(password,16))
        return ciphertext