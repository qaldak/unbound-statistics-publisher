import logging
from socket import gethostname

logger = logging.getLogger(__name__)


def get_hostname(lettercase: str) -> str:
    """
    __get_hostname__("<lower|upper>")

    Returns the hostname in desired letter case.
    """

    if lettercase == "lower":
        hostname = gethostname().lower()
    elif lettercase == "upper":
        hostname = gethostname().upper()
    else:
        logger.error("Letter case undefined!")
        raise ValueError("Letter case undefined! Possible values: '<lower|upper>'")

    return hostname
