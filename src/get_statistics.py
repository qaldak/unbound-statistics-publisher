import json
import logging

from python_on_whales import docker

logger = logging.getLogger(__name__)


class Collector:

    @staticmethod
    def __convert_to_json(stats):
        tmp_stats = stats.replace("t", '{"t', 1).replace("=", '":').replace("\n", ',"')
        tmp_stats += '}'
        try:
            json_stats = json.loads(tmp_stats)
            return json_stats
        except json.decoder.JSONDecodeError as e:
            logger.error(f"Not possible to create json statistics. Exception: {e}, \n "
                         f"stats: {tmp_stats}")

    @staticmethod
    def get_statistics(container, reset_unbound_stats: bool = False):
        if reset_unbound_stats:
            stats_param = "stats"
        else:
            stats_param = "stats_noreset"

        logger.debug(f"Set <stats_param> = '{stats_param}'")

        stats = (docker.execute(container, ["unbound-control", stats_param]))
        stats_json = Collector.__convert_to_json(stats)
        if type(stats_json) == dict:
            logger.debug(f"Received unbound statistics: {stats_json}")
            return stats_json
        else:
            logger.error(f"No json statistics available. type = {type(stats_json)}")
