from get_metrics import get_metrics
from check_container import Container
from socket import gethostname

import logging

logger = logging.getLogger(__name__)


def __get_hostname():
    hostname = gethostname()
    return hostname.lower()


def main():
    logger.debug("Start")

    if Container(f"unbound_{__get_hostname()}").is_running():
        print("huhu")
    else:
        print("bar")


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING, filename="./unbound-metrics.log", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    main()
