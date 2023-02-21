from python_on_whales import docker

import json
import logging

logger = logging.getLogger(__name__)


def __convert_to_json(stats):
    stats = stats.replace("t", '{"t', 1).replace("=", '":').replace("\n", ',"')
    stats += '}'
    try:
        json_stats = json.loads(stats)
        return json_stats
    except json.decoder.JSONDecodeError as e:
        logger.error(f"Not possible to create json statistics. Exception: {e}, \n "
                     f"stats: {stats}")


def get_statistics(container: str):
    stats = (docker.execute(container, ["unbound-control", "stats_noreset"]))
    stats_json = __convert_to_json(stats)
    if type(stats_json) == dict:
        logger.debug(f"Received unbound statistics: {stats_json}")
        return stats_json
    else:
        logger.error(f"No json statistics available. type = {type(stats_json)}")
