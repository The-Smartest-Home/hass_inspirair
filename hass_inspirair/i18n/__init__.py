import gettext
from pathlib import Path
from typing import Any

from hass_inspirair.env_config import EnvConfig

APP = Path(__file__).parent.parent.name
DIR = Path(__file__).parent


def translate(*args: Any, **kwargs: Any) -> str:
    try:
        lang = gettext.translation(
            APP, localedir=DIR, languages=[EnvConfig.HI_CFG_LANGUAGE], fallback=False
        )
        return lang.gettext(*args, **kwargs)
    except FileNotFoundError:
        pass

    lang = gettext.translation(APP, localedir=DIR, languages=["de"], fallback=False)
    return lang.gettext(*args, **kwargs)


_ = translate
