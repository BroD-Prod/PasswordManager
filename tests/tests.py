import unittest
import src.login_password_hash as login_password_hash

class TestPassword(unittest.TestCase):
    def test_hash_login_password_returns_bytes(self):
        password_manager = login_password_hash.Login_Password()
        result = password_manager.hash_password("securepassword")
        self.assertIsInstance(result, str)

    def test_stored_hashed_password(self, test_password="password"):
        password_manager = login_password_hash.Login_Password()
        hash = password_manager.hash_password(test_password)
        self.assertIsNot(test_password, password_manager.password_hash[0])