from unittest import TestCase
from unittest.mock import patch

from python_on_whales import docker
from src.check_container import Container


class TestDockerContainerRunning(TestCase):

    def test_container_running(self):
        with docker.run("busybox", ["sleep", "infinity"], detach=True, remove=True, name="busybox") as c:
            assert Container("busybox").is_running() is True

    @patch("src.check_container.docker.ps", return_value=True)
    def test_container_running_mock(self, mock_container_state):
        assert Container("Foo").is_running() is True

    @patch("src.check_container.docker.ps", return_value=False)
    def test_container_not_running(self, mock_container_state):
        assert Container("Foo").is_running() is False
