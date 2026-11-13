import argparse
import logging
import os
import sys

from python_on_whales import DockerException

from src.container import Container
from src.get_statistics import Collector
from src.send_statistics import Publisher

logger = logging.getLogger(__name__)


def main(receiver_ip, reset_unbound_stats: bool) -> bool:
    """
    Collect the unbound statistics and publish them to the receiver.

    Returns True if the statistics were sent, otherwise False. Details are written to the log.
    """
    try:
        collector_cntnr = Container.determine_container_name("unbound")
        publisher_cntnr = Container.determine_container_name("mosquitto")
    except (ValueError, DockerException):
        logger.error("Unbound or Mosquitto container could not be determined. Check log for details.")
        return False

    logger.debug(f"Param reset_unbound_stats = {reset_unbound_stats}")
    logger.debug(f"Provide statistics for Docker container '{collector_cntnr}'")

    if not (Container(collector_cntnr).is_running() and Container(publisher_cntnr).is_running()):
        logger.error("A Container is missing or not running. Check log for details.")
        return False

    unbound_stats = Collector.get_statistics(collector_cntnr, reset_unbound_stats)
    if not unbound_stats:
        logger.error("No unbound statistics available, nothing sent. Check log for details.")
        return False

    if not Publisher.send_statistics(receiver_ip, unbound_stats, publisher_cntnr):
        logger.error("Unbound statistics failed. Check log for details.")
        return False

    logger.debug("Unbound statistics sent successful.")
    return True


def parse_args(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("receiver_ip", help="IP address of the message receiver, e.g. MQTT Broker")
    parser.add_argument("-nr", "--no-reset", action="store_false", dest="reset_unbound_stats",
                        help="Do not reset unbound statistics")
    parser.add_argument("--debug", action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.WARNING,
                        help="Set loglevel to DEBUG")
    return parser.parse_args(argv)


if __name__ == "__main__":
    args = parse_args()

    logdir = "log"
    if not os.path.isdir(logdir):
        os.makedirs(logdir)

    logging.basicConfig(level=args.loglevel, filename=f"{logdir}/unbound-stats.log",
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Exit code 1 on failure, so cron or other schedulers can detect it
    sys.exit(0 if main(args.receiver_ip, args.reset_unbound_stats) else 1)
