import asyncio
import logging
import sys

from ha_aldes.i18n import APP
from ha_aldes.main import main_loop


def _init_logger() -> None:
    logger = logging.getLogger(APP)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(name)s - (%(filename)s:%(lineno)d) - %(levelname)s - %(message)s"
        )
    )
    logger.addHandler(handler)


_init_logger()
loop = asyncio.get_event_loop()
loop.run_until_complete(main_loop(loop))
loop.close()
