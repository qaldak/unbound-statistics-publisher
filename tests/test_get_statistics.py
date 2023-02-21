from unittest import TestCase
from unittest.mock import patch

from src.get_statistics import get_statistics


class TestCollectUnboundStatistics(TestCase):

    @patch("src.get_metrics.docker.execute", return_value=(open("fixtures/unbound_stats.file").read()))
    def test_get_unbound_stats(self, unbound_stats):
        stats_json = get_statistics("unbound_foo")
        self.assertIsInstance(stats_json, dict)
