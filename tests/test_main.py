import logging
from unittest import TestCase
from unittest.mock import patch

from python_on_whales import DockerException

from src.main import main, parse_args


@patch("src.main.Publisher.send_statistics", return_value=True)
@patch("src.main.Collector.get_statistics", return_value='{"Foo": "Bar"}')
@patch("src.main.Container.is_running", return_value=True)
@patch("src.main.Container.determine_container_name", side_effect=["unbound-test", "mosquitto-test"])
class TestProvideStatistics(TestCase):

    def test_happy_flow(self, mock_name, mock_running, mock_stats, mock_send):
        with self.assertLogs("src.main", level="DEBUG") as log:
            result = main("127.0.0.1", False)

        self.assertTrue(result)
        mock_stats.assert_called_once_with("unbound-test", False)
        mock_send.assert_called_once_with("127.0.0.1", '{"Foo": "Bar"}', "mosquitto-test")
        self.assertIn("DEBUG:src.main:Unbound statistics sent successful.", log.output)

    def test_container_not_running(self, mock_name, mock_running, mock_stats, mock_send):
        mock_running.return_value = False

        with self.assertLogs("src.main", level="ERROR") as log:
            result = main("127.0.0.1", True)

        self.assertFalse(result)
        self.assertEqual(log.output,
                         ["ERROR:src.main:A Container is missing or not running. Check log for details."])
        mock_stats.assert_not_called()
        mock_send.assert_not_called()

    def test_no_statistics_are_not_sent(self, mock_name, mock_running, mock_stats, mock_send):
        mock_stats.return_value = None

        with self.assertLogs("src.main", level="ERROR") as log:
            result = main("127.0.0.1", True)

        self.assertFalse(result)
        self.assertEqual(log.output,
                         ["ERROR:src.main:No unbound statistics available, nothing sent. Check log for details."])
        mock_send.assert_not_called()

    def test_send_failed(self, mock_name, mock_running, mock_stats, mock_send):
        mock_send.return_value = False

        with self.assertLogs("src.main", level="ERROR") as log:
            result = main("127.0.0.1", True)

        self.assertFalse(result)
        self.assertEqual(log.output, ["ERROR:src.main:Unbound statistics failed. Check log for details."])

    def test_container_not_found(self, mock_name, mock_running, mock_stats, mock_send):
        mock_name.side_effect = ValueError("No container available with name 'unbound'")

        with self.assertLogs("src.main", level="ERROR"):
            result = main("127.0.0.1", True)

        self.assertFalse(result)
        mock_stats.assert_not_called()
        mock_send.assert_not_called()

    def test_docker_error(self, mock_name, mock_running, mock_stats, mock_send):
        mock_name.side_effect = DockerException(command_launched=["docker", "ps"], return_code=1)

        with self.assertLogs("src.main", level="ERROR"):
            result = main("127.0.0.1", True)

        self.assertFalse(result)
        mock_send.assert_not_called()


class TestMainArguments(TestCase):

    def test_start_without_param(self):
        with self.assertRaises(TypeError) as err:
            main()
        self.assertEqual(str(err.exception), "main() missing 2 required positional arguments: 'receiver_ip' and "
                                             "'reset_unbound_stats'")

    def test_parse_args_defaults(self):
        args = parse_args(["192.0.2.1"])
        self.assertEqual(args.receiver_ip, "192.0.2.1")
        self.assertTrue(args.reset_unbound_stats)
        self.assertEqual(args.loglevel, logging.WARNING)

    def test_parse_args_options(self):
        args = parse_args(["192.0.2.1", "--no-reset", "--debug"])
        self.assertFalse(args.reset_unbound_stats)
        self.assertEqual(args.loglevel, logging.DEBUG)
