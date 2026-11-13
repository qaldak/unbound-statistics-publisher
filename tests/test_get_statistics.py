import json
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from python_on_whales import DockerException

from src.get_statistics import Collector

FIXTURE = Path(__file__).parent / "fixtures" / "unbound_stats.file"


class TestCollectUnboundStatistics(TestCase):

    def test_get_unbound_stats(self):
        with patch("src.get_statistics.docker.execute", return_value=FIXTURE.read_text()):
            stats_json = Collector.get_statistics("foo")

        self.assertIsInstance(stats_json, str)
        self.assertNotRegex(stats_json, r"'")

        stats = json.loads(stats_json)
        self.assertEqual(stats["thread0.num.queries"], 20)
        self.assertEqual(stats["thread0.recursion.time.avg"], 0.173971)

    def test_debug_messages(self):
        with patch("src.get_statistics.docker.execute", return_value="a=1\nb=2.5"):
            with self.assertLogs("src.get_statistics", level="DEBUG") as log:
                Collector.get_statistics("foo")

        self.assertIn("DEBUG:src.get_statistics:Converted unbound statistics: {'a': 1, 'b': 2.5}", log.output)
        self.assertIn('DEBUG:src.get_statistics:JSONified unbound statistics: {"a": 1, "b": 2.5}', log.output)

    def test_trailing_newline(self):
        with patch("src.get_statistics.docker.execute", return_value="thread0.num.queries=1\nthread0.num.cachehits=2\n"):
            stats_json = Collector.get_statistics("foo")

        self.assertEqual(json.loads(stats_json), {"thread0.num.queries": 1, "thread0.num.cachehits": 2})

    def test_non_numeric_value_is_kept_as_string(self):
        with patch("src.get_statistics.docker.execute", return_value="a=1\nb=nan\nc=text"):
            stats_json = Collector.get_statistics("foo")

        self.assertEqual(json.loads(stats_json), {"a": 1, "b": "nan", "c": "text"})

    def test_garbage_returns_none(self):
        with patch("src.get_statistics.docker.execute", return_value="error: connection refused"):
            with self.assertLogs("src.get_statistics", level="ERROR"):
                self.assertIsNone(Collector.get_statistics("foo"))

    def test_empty_output_returns_none(self):
        with patch("src.get_statistics.docker.execute", return_value=""):
            with self.assertLogs("src.get_statistics", level="ERROR"):
                self.assertIsNone(Collector.get_statistics("foo"))

    def test_docker_error_returns_none(self):
        error = DockerException(command_launched=["docker", "exec"], return_code=1, stderr=b"unbound is down")
        with patch("src.get_statistics.docker.execute", side_effect=error):
            with self.assertLogs("src.get_statistics", level="ERROR"):
                self.assertIsNone(Collector.get_statistics("foo"))

    def test_reset_parameter(self):
        with patch("src.get_statistics.docker.execute", return_value="a=1") as execute:
            Collector.get_statistics("foo", True)
            execute.assert_called_with("foo", ["unbound-control", "stats"])

            Collector.get_statistics("foo", False)
            execute.assert_called_with("foo", ["unbound-control", "stats_noreset"])
