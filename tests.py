import unittest
import password

class TestPassword(unittest.TestCase):
    def test_hash_password_returns_bytes(self):
        password_manager = password.Password()
        result = password_manager.hash_password("securepassword")
        self.assertIsInstance(result, bytes)