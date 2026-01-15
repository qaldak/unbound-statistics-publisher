import logging
from unittest import TestCase
from unittest.mock import patch

from src.main import main


class TestProvideStatistics(TestCase):

    @patch("src.main.Container.determine_container_name", return_value="unbound-test")
    @patch("src.send_statistics.Publisher.send_statistics", return_value=True)
    @patch("src.get_statistics.Collector.get_statistics", return_value='{"Foo": "Bar"}')
    @patch("src.container.Container.is_running", return_value=True)
    def test_happy_flow(self, cntnr_name, cntnr_running, stats, msg_sent):
        with self.assertLogs("__main__", level="DEBUG") as log:
            logging.getLogger("__main__").debug("Unbound statistics sent successful.")

        result = main("127.0.0.1", False)
        self.assertEqual(result, None)
        self.assertEqual(log.output, ["DEBUG:__main__:Unbound statistics sent successful."])

    @patch("src.main.Container.determine_container_name", return_value="unbound-test")
    @patch("src.container.Container.is_running", return_value=False)
    def test_failed(self, cntnr_name, cntnr_running):
        with self.assertLogs("__main__", level="ERROR") as log:
            logging.getLogger("__main__").error("A Container is missing or not running. Check log for details.")
            main("127.0.0.1", True)
        self.assertEqual(log.output, ["ERROR:__main__:A Container is missing or not running. Check log for details."])

    def test_start_without_param(self):
        with self.assertRaises(TypeError) as err:
            main()
        self.assertEqual(str(err.exception), "main() missing 2 required positional arguments: 'receiver_ip' and "
                                             "'reset_unbound_stats'")
