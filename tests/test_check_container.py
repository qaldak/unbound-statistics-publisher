from unittest import TestCase, mock
from unittest.mock import patch

from src.check_container import Container


class Test(TestCase):

    @patch("src.check_container.Container.call_container")
    def test_check_container(self, mock_container):
        # mock_container.return_value = "status='running' running=True paused=False restarting=False oom_killed=False dead=False pid=6938 exit_code=0 error='' started_at=datetime.datetime(2023, 2, 10, 8, 15, 51, 574963, tzinfo=datetime.timezone.utc) finished_at=datetime.datetime(1, 1, 1, 0, 0, tzinfo=datetime.timezone.utc) health=None"

        mock_container.return_value = mock.Mock(state=[{"status": "running"}])
        container = Container("busybox")
        container_running = container.is_running()
        assert container_running is True

    ''' def test_check_container_failed(self):
        container = Container("Foo")
        container_running = container.is_running()
        assert container_running is False

    def test_check_container_error(self):
        container = Container("Foo")
        container_running = container.is_running()
        assert container_running is False
        '''
