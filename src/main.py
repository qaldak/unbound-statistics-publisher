from get_metrics import get_metrics
from check_container import Container
from socket import gethostname

import logging


def get_hostname():
    hostname = gethostname()
    print("Hostname is:", hostname.lower())


def main():
    get_metrics()
    get_hostname()
    container = Container("opensearch-opensearch-1")
    if container.is_running():
        print("huhu")
    else:
        print("bar")


if __name__ == '__main__':
    main()
