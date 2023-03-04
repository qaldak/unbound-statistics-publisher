import logging

from python_on_whales import docker, DockerException

from src.get_hostname import get_hostname

logger = logging.getLogger(__name__)


class Publisher:

    @staticmethod
    def send_statistics(receiver_ip: str, stats: dict, publisher_cntnr: str) -> bool:
        if not isinstance(stats, dict):
            raise TypeError

        __topic__ = f"statistics/unbound/{get_hostname('upper')}"

        try:
            docker.execute(publisher_cntnr,
                           [f"mosquitto_pub", "-h", f"{receiver_ip}", "-q", "1", "-t", f"{__topic__}", "-m",
                            f"{stats}"])
            logger.debug("Send statistics to MQTT broker successful.")
            success = True

        except DockerException as e:
            logger.error(
                f"Send statistics to MQTT broker failed. {DockerException.__name__}: Exit code {e.return_code}, {e.stderr.strip()}")
            logger.error(
                f"DockerException: {e}")
            success = False

        return success
