import gettext
from pathlib import Path

APP = Path(__file__).parent.parent.name
DIR = Path(__file__).parent

lang = gettext.translation(APP, localedir=DIR, languages=["en", "de"], fallback=False)

_ = lang.gettext
