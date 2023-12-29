import gettext
from pathlib import Path
from typing import Any

APP = Path(__file__).parent.parent.name
DIR = Path(__file__).parent


def translate(*args: Any, **kwargs: Any) -> str:
    try:
        lang = gettext.translation(APP, localedir=DIR, fallback=False)
        return lang.gettext(*args, **kwargs)
    except FileNotFoundError:
        pass

    lang = gettext.translation(APP, localedir=DIR, languages=["de"], fallback=False)
    return lang.gettext(*args, **kwargs)


_ = translate
