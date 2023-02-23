from check_container import Container
from get_statistics import get_statistics
from send_statistics import send_statistics
from socket import gethostname

import argparse
import logging

logger = logging.getLogger(__name__)


def __get_hostname():
    return gethostname().lower()


def main(mqtt_broker_ip):
    print(type(mqtt_broker_ip))
    unbound_container = f"unbound_{__get_hostname()}"
    mosquitto_container = f"mosquitto_{__get_hostname()}"

    logger.debug(f"Get statistics for Docker container '{unbound_container}'")

    if Container(unbound_container).is_running() and Container(mosquitto_container).is_running():
        unbound_stats = get_statistics(unbound_container)
        send_statistics(mqtt_broker_ip, unbound_stats)
        logger.debug(f"Unbound statistics sent successful.")
    else:
        logger.error(f"A Container is missing or not running. Check log for details.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("mqtt_broker_ip", help="IP address of MQTT Broker")
    parser.add_argument("--debug", action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.WARNING,
                        help="Set loglevel to DEBUG")
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel, filename="./unbound-stats.log",
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    print(logging.getLevelName(args.loglevel))
    main(args.mqtt_broker_ip)
