import json
import logging
import math

from python_on_whales import docker, DockerException

logger = logging.getLogger(__name__)


class Collector:

    @staticmethod
    def __parse_value(value: str):
        """Return value as int or float if possible, otherwise as string."""
        for convert in (int, float):
            try:
                number = convert(value)
            except ValueError:
                continue
            # 'nan' and 'inf' are no valid JSON numbers
            if isinstance(number, float) and not math.isfinite(number):
                break
            return number
        return value

    @staticmethod
    def __convert_to_json(stats: str) -> str | None:
        """
        Convert the 'key=value' lines of 'unbound-control stats' to a JSON string.

        Returns None if no statistics could be extracted.
        """
        data = {}
        for line in stats.splitlines():
            key, separator, value = line.partition("=")
            key = key.strip()
            if not separator or not key:
                if line.strip():
                    logger.warning(f"Skip unexpected line in unbound statistics: {line!r}")
                continue
            data[key] = Collector.__parse_value(value.strip())

        if not data:
            logger.error(f"Not possible to create json statistics. stats: {stats!r}")
            return None

        logger.debug(f"Converted unbound statistics: {data}")

        json_stats = json.dumps(data)
        logger.debug(f"JSONified unbound statistics: {json_stats}")
        return json_stats

    @staticmethod
    def get_statistics(container, reset_unbound_stats: bool = False) -> str | None:
        if reset_unbound_stats:
            stats_param = "stats"
        else:
            stats_param = "stats_noreset"

        logger.debug(f"Set <stats_param> = '{stats_param}'")

        try:
            stats = docker.execute(container, ["unbound-control", stats_param])
        except DockerException as e:
            logger.error(f"unbound-control {stats_param} failed. {DockerException.__name__}: "
                         f"Exit code {e.return_code}, {(e.stderr or '').strip()}")
            return None

        stats_json = Collector.__convert_to_json(stats)
        if not stats_json:
            logger.error("No json statistics available.")
            return None

        logger.debug(f"Received unbound statistics: {stats_json}")
        return stats_json
