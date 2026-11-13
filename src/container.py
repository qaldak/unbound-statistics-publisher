import logging

from python_on_whales import docker, DockerException

logger = logging.getLogger(__name__)


class Container:
    def __init__(self, name):
        self.name = name

    def __log_container_info(self):
        for container in docker.ps(all=True, filters=[("name", self.name)]):
            logger.debug(f"Container info for '{self.name}': {container.state}")

    def is_running(self) -> bool:
        try:
            if docker.ps(filters=[("name", self.name), ("status", "running")]):
                logger.debug(f"Container {self.name} is running")
                return True
            else:
                logger.warning(f"Docker Container '{self.name}' not found or is not running")
                if logger.isEnabledFor(logging.DEBUG):
                    self.__log_container_info()
                return False

        except DockerException as e:
            logger.error(f"{DockerException.__name__}: Exit code {e.return_code}, {(e.stderr or '').strip()}")
            return False

    @staticmethod
    def determine_container_name(name: str) -> str:
        search_name = name.lower()

        if search_name not in ["mosquitto", "unbound"]:
            logger.error(f"Unsupported container: {search_name}")
            raise ValueError(f"Unsupported container: {search_name}")

        try:
            logger.debug(f"Searching for container: {search_name}")
            # Docker's name filter matches substrings (e.g. 'my-unbound' for 'unbound'),
            # so only keep containers whose name really starts with the searched name.
            containers = docker.ps(filters=[("name", search_name)])
            cntr_names = sorted(c.name for c in containers if c.name.lower().startswith(search_name))

            if not cntr_names:
                logger.error(f"No container available with name '{search_name}'")
                raise ValueError(f"No container available with name '{search_name}'")

            if len(cntr_names) > 1:
                logger.warning(f"Multiple containers found for '{search_name}': {cntr_names}. "
                               f"Using '{cntr_names[0]}'")

            cntr_name = cntr_names[0]
            logger.debug(f"Container found: {cntr_name}")
            return cntr_name

        except DockerException as e:
            logger.error(f"Docker error while searching for  '{search_name}': {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error search for '{search_name}': {e}")
            raise
