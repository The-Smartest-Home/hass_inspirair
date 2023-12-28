import gettext

from pathlib import Path

APP = Path(__file__).parent.parent.name
DIR = Path(__file__).parent.name


lang = gettext.translation(APP, localedir=DIR, fallback=False)
_ = lang.gettext
