import argparse
import logging

from check_container import Container
from get_hostname import get_hostname
from get_statistics import Collector
from send_statistics import Publisher

logger = logging.getLogger(__name__)


def main(receiver_ip, reset_unbound_stats: bool):
    collector_cntnr = f"unbound_{get_hostname('lower')}"
    publisher_cntnr = f"mosquitto_{get_hostname('lower')}"

    logger.debug(f"Param reset_unbound_stats = {reset_unbound_stats}")
    logger.debug(f"Provide statistics for Docker container '{collector_cntnr}'")

    if Container(collector_cntnr).is_running() and Container(publisher_cntnr).is_running():
        unbound_stats = Collector.get_statistics(collector_cntnr, reset_unbound_stats)
        statistic_sent = Publisher.send_statistics(receiver_ip, unbound_stats, publisher_cntnr)
        if statistic_sent:
            logger.debug(f"Unbound statistics sent successful.")
        else:
            logger.error(f"Unbound statistics failed. Check log for details.")
    else:
        logger.error(f"A Container is missing or not running. Check log for details.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("receiver_ip", help="IP address of the message receiver, e.g. MQTT Broker")
    parser.add_argument("-nr", "--no-reset", action="store_false", dest="reset_unbound_stats",
                        help="Do not reset unbound statistics")
    parser.add_argument("--debug", action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.WARNING,
                        help="Set loglevel to DEBUG")
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel, filename="../log/unbound-stats.log",
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    main(args.receiver_ip, args.reset_unbound_stats)
