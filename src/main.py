from get_statistics import get_metrics
from check_container import Container
from socket import gethostname

import logging

logger = logging.getLogger(__name__)


def __get_hostname():
    hostname = gethostname()
    return hostname.lower()


def main():
    unbound_container = f"unbound_{__get_hostname()}"
    logger.debug(f"Get statistics for Docker container '{unbound_container}'")

    if Container(unbound_container).is_running():
        unbound_stats = get_metrics(unbound_container)
        print("huhu")
        print(f"{unbound_stats}")
    else:
        print("bar")


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING, filename="./unbound-stats.log",
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    main()
