from pyrake.project import crawler
stats = crawler.stats

import warnings
from pyrake.exceptions import pyrakeDeprecationWarning
warnings.warn("Module `pyrake.stats` is deprecated, use `crawler.stats` attribute instead",
    pyrakeDeprecationWarning, stacklevel=2)
