from unittest import TestCase
from unittest.mock import patch

from src.get_statistics import Collector


class TestCollectUnboundStatistics(TestCase):

    @patch("src.get_statistics.docker.execute",
           return_value=(open("fixtures/unbound_stats.file").read()))
    def test_get_unbound_stats(self, unbound_stats):
        stats_json = Collector.get_statistics("foo")
        self.assertIsInstance(stats_json, dict)
