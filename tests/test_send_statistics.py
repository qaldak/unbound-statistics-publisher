import logging
from unittest import TestCase
from unittest.mock import patch

from python_on_whales import DockerException

from src.send_statistics import Publisher


class TestSendStatistics(TestCase):

    @patch("send_statistics.docker.execute", side_effect=DockerException(return_code=1,
                                                                         command_launched="/usr/bin/docker exec publisher_cntnr pub -h 127.0.0.1 -q 1 -t statistics/foo/bar -m {'Foo':'Bar'}",
                                                                         stderr=b'f\x00o\x00o\x00b\x00a\x00r\x00b\x00a\x00z\x00'))
    def test_send_msg_failed(self, error):
        stats = {"Foo": "Bar"}
        success = Publisher.send_statistics("127.0.0.1", stats, "publisher_cntnr")
        self.assertRaises(DockerException)
        self.assertFalse(success)

    @patch("send_statistics.docker.execute", return_value=True)
    def test_send_msg_successful(self, result):
        stats = {"thread0.num.queries": 1102}
        self.assertTrue(Publisher.send_statistics("127.0.0.1", stats, "publisher_cntnr"))

    def test_send_not_json_msg(self):
        stats = "Only 'dict' is allowed"
        self.assertRaises(TypeError, lambda: Publisher.send_statistics("127.0.0.1", stats, "publisher_cntnr"))
