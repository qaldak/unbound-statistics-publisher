from unittest import TestCase

from src.get_hostname import get_hostname


class TestGetHostname(TestCase):
    def test_hostname_lowercase(self):
        result = get_hostname('lower')
        self.assertTrue(result.islower())

    def test_hostname_uppercase(self):
        result = get_hostname('upper')
        self.assertTrue(result.isupper())

    def test_hostname_exception(self):
        self.assertRaises(TypeError, lambda: get_hostname("what?"))
