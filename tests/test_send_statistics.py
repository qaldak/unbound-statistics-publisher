from unittest import TestCase
from unittest.mock import patch

from python_on_whales import DockerException
from src.send_statistics import send_statistics


class TestSendStatistics(TestCase):
    @patch("src.send_statistics.docker.execute", return_value=None)
    def test_send_msg_successful(self, result):
        stats = {"thread0.num.queries": 1102}
        self.assertEqual(send_statistics("192.168.1.10", stats), None)

    @patch("src.send_statistics.docker.execute", return_value=DockerException)
    def test_send_msg_failed(self, error):
        stats = {"thread0.num.queries": 1102}
        send_statistics("192.168.1.10", stats)
        self.assertRaises(DockerException)

    def test_send_not_json_msg(self):
        stats = "Only 'dict' is allowed"
        self.assertRaises(TypeError, lambda: send_statistics("192.168.1.10", stats))


if __name__ == '__main__':
    unittest.main()
