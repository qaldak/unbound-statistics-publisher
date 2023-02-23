import logging

from socket import gethostname

from python_on_whales import docker, DockerException

logger = logging.getLogger(__name__)


def __get_hostname(lettercase: str) -> str:
    """
    __get_hostname__("<lower|upper>")

    Returns the hostname in desired letter case.
    """

    match lettercase:
        case "lower":
            hostname = gethostname().lower()
        case "upper":
            hostname = gethostname().upper()
        case _:
            logger.error(f"Letter case undefined!")
            raise TypeError("Letter case undefined! Possible values: '<lower|upper>'")

    return hostname


def send_statistics(mqtt_broker_ip: str, stats: dict):
    if not isinstance(stats, dict):
        raise TypeError

    __topic__ = f"statistics/unbound/{__get_hostname('upper')}"

    try:
        docker.execute(f"mosquitto_{__get_hostname('lower')}",
                       [f"mosquitto_pub", "-h", f"{mqtt_broker_ip}", "-q", "1", "-t", f"{__topic__}", "-m", f"{stats}"])
        logger.debug("Send statistics to MQTT broker successful.")
        exitcode = 0

    except DockerException as e:
        logger.error(
            f"Send statistics to MQTT broker failed. {DockerException.__name__}: Exit code {e.return_code}, {e.stderr.strip()}")
        logger.error(
            f"DockerException: {e}")
        exitcode = e.return_code

    return exit(exitcode)
