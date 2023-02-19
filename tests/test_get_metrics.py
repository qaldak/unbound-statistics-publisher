from unittest import TestCase
from unittest.mock import patch

import pytest as pytest

from src.get_metrics import get_metrics


class TestCollectUnboundMetrics(TestCase):

    @pytest.fixture
    def metrics():
        return True

    def test_get_unbound_metrics(self, metrics):
        assert metrics is True
