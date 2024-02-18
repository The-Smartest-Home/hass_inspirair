import argparse
import asyncio
import logging
import os
import sys

from hass_inspirair.env_config import EnvConfig
from hass_inspirair.i18n import APP
from hass_inspirair.main import main_loop


class LogFormatter(logging.Formatter):
    LEVEL_FORMATS = {
        logging.DEBUG: "\x1b[2m   DEBUG\x1b[0m",
        logging.INFO: "    INFO",
        logging.WARNING: "\x1b[33mWARNING\x1b[0m",
        logging.ERROR: "\x1b[31m   ERROR\x1b[0m",
        logging.CRITICAL: "\x1b[31mCRITICAL\x1b[0m",
    }
    LEVEL_FORMATS_COLORS = {
        logging.DEBUG: "\x1b[2m",
        logging.INFO: "",
        logging.WARNING: "\x1b[33m",
        logging.ERROR: "\x1b[31m",
        logging.CRITICAL: "\x1b[41m",
    }

    def _format(self, levelno: int) -> str:
        return (
            f"{self.LEVEL_FORMATS_COLORS.get(levelno)}%(asctime)s  %(name)30.30s (%(filename)10.10s:%(lineno)4.d) "
            f"%(levelname)8.8s %(message)s \x1b[0m"
        )

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self._format(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def _init_logger() -> None:
    logger = logging.getLogger(APP)
    logger.setLevel(EnvConfig.HI_CFG_LOGLEVEL)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(LogFormatter())
    logger.addHandler(handler)


def config_file(config_path: str) -> str:
    from os.path import exists

    if not exists(config_path):
        raise argparse.ArgumentTypeError("'%s' does not exists" % config_path)
    os.environ["HI_CFG_FILE"] = config_path
    return config_path


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", type=config_file)
args = parser.parse_args()


def main() -> None:
    _init_logger()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_loop(loop))
    loop.close()


if __name__ == "__main__":
    main()
