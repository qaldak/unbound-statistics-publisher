from unittest import TestCase
from unittest.mock import patch, Mock

from python_on_whales import docker

from src.container import Container


class TestDockerContainerRunning(TestCase):

    def test_container_running(self):
        with docker.run("busybox", ["sleep", "infinity"], detach=True, remove=True, name="busybox") as c:
            assert Container("busybox").is_running() is True

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

    @patch("get_hostname.gethostname", return_value="bar")
    def test_determine_container_name_error(self, mock_hostname):
        with self.assertRaises(ValueError) as err:
            cnt_name = Container.determine_container_name("Foo")
        self.assertEqual(str(err.exception), "Unsupported container: foo")
