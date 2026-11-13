from unittest import TestCase
from unittest.mock import patch

from python_on_whales import DockerException

from src.send_statistics import Publisher


class TestSendStatistics(TestCase):

    @patch("src.send_statistics.get_hostname", return_value="FOOHOST")
    @patch("src.send_statistics.docker.execute", return_value=True)
    def test_send_msg_successful(self, mock_execute, mock_hostname):
        stats = '{"thread0.num.queries": 1102}'

        self.assertTrue(Publisher.send_statistics("127.0.0.1", stats, "publisher_cntnr"))

        mock_execute.assert_called_once_with(
            "publisher_cntnr",
            ["mosquitto_pub", "-h", "127.0.0.1", "-q", "1", "-t", "statistics/unbound/FOOHOST", "-m", stats])

    @patch("src.send_statistics.docker.execute")
    def test_send_msg_failed(self, mock_execute):
        mock_execute.side_effect = DockerException(
            command_launched=["docker", "exec", "publisher_cntnr", "mosquitto_pub"],
            return_code=1,
            stderr=b"Error: Connection refused")

        with self.assertLogs("src.send_statistics", level="ERROR") as log:
            success = Publisher.send_statistics("127.0.0.1", '{"Foo": "Bar"}', "publisher_cntnr")

        self.assertFalse(success)
        self.assertIn("Connection refused", log.output[0])
