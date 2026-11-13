import uuid
from unittest import TestCase, skipUnless
from unittest.mock import patch, Mock

from python_on_whales import docker, DockerException

from src.container import Container


def docker_available() -> bool:
    """True if a Docker daemon can be reached."""
    try:
        docker.info()
    except Exception:  # no docker binary, daemon not running, missing permission, ...
        return False
    return True


class TestDockerContainerRunning(TestCase):

    @skipUnless(docker_available(), "Docker daemon not available")
    def test_container_running(self):
        # unique name, so a container left over from an earlier run cannot interfere
        name = f"busybox-test-{uuid.uuid4().hex[:8]}"
        with docker.run("busybox", ["sleep", "infinity"], detach=True, remove=True, name=name):
            self.assertTrue(Container(name).is_running())

    @patch("src.container.docker.ps", return_value=True)
    def test_container_running_mock(self, mock_container_state):
        assert Container("Foo").is_running() is True

    @patch("src.container.docker.ps", return_value=False)
    def test_container_not_running(self, mock_container_state):
        assert Container("Foo").is_running() is False

    @patch("src.container.docker.ps")
    def test_determine_container_name_unbound(self, mock_docker_ps):
        mock_container = Mock()
        mock_container.id = '12345678'
        mock_container.name = 'unbound-bar'

        mock_docker_ps.return_value = [mock_container]

        cnt_name = Container.determine_container_name("unbound")
        self.assertEqual(cnt_name, "unbound-bar")

    @patch("src.container.docker.ps")
    def test_determine_container_name_mosquitto(self, mock_docker_ps):
        mock_container = Mock()
        mock_container.id = '12345678'
        mock_container.name = 'mosquitto-bar'

        mock_docker_ps.return_value = [mock_container]

        cnt_name = Container.determine_container_name("mosquitto")
        self.assertEqual(cnt_name, "mosquitto-bar")

    def test_determine_container_name_error(self):
        with self.assertRaises(ValueError) as err:
            Container.determine_container_name("Foo")
        self.assertEqual(str(err.exception), "Unsupported container: foo")

    @staticmethod
    def _container(name):
        container = Mock()
        container.name = name
        return container

    @patch("src.container.docker.ps")
    def test_determine_container_name_ignores_substring_matches(self, mock_docker_ps):
        mock_docker_ps.return_value = [self._container("my-unbound-exporter"), self._container("unbound-bar")]

        self.assertEqual(Container.determine_container_name("unbound"), "unbound-bar")

    @patch("src.container.docker.ps")
    def test_determine_container_name_only_substring_match(self, mock_docker_ps):
        mock_docker_ps.return_value = [self._container("my-unbound-exporter")]

        with self.assertRaises(ValueError) as err:
            Container.determine_container_name("unbound")
        self.assertEqual(str(err.exception), "No container available with name 'unbound'")

    @patch("src.container.docker.ps", return_value=[])
    def test_determine_container_name_not_found(self, mock_docker_ps):
        with self.assertRaises(ValueError):
            Container.determine_container_name("mosquitto")

    @patch("src.container.docker.ps")
    def test_determine_container_name_multiple_is_deterministic(self, mock_docker_ps):
        mock_docker_ps.return_value = [self._container("unbound-b"), self._container("unbound-a")]

        with self.assertLogs("src.container", level="WARNING"):
            self.assertEqual(Container.determine_container_name("unbound"), "unbound-a")

    @patch("src.container.docker.ps")
    def test_is_running_docker_error(self, mock_docker_ps):
        mock_docker_ps.side_effect = DockerException(command_launched=["docker", "ps"], return_code=1,
                                                     stderr=b"daemon not running")

        with self.assertLogs("src.container", level="ERROR"):
            self.assertIs(Container("Foo").is_running(), False)
