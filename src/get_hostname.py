import logging
from socket import gethostname

logger = logging.getLogger(__name__)


def get_hostname(lettercase: str) -> str:
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
