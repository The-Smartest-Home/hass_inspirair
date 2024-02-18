import argparse
import asyncio
import logging
import os
import sys

from hass_inspirair.env_config import EnvConfig
from hass_inspirair.i18n import APP
from hass_inspirair.main import main_loop


def _init_logger() -> None:
    logger = logging.getLogger(APP)
    logger.setLevel(EnvConfig.HI_CFG_LOGLEVEL)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(name)s - (%(filename)s:%(lineno)d) - %(levelname)s - %(message)s"
        )
    )
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
