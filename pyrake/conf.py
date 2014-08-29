# This module is kept for backwards compatibility, so users can import
# pyrake.conf.settings and get the settings they expect

import sys

if 'pyrake.cmdline' not in sys.modules:
    from pyrake.utils.project import get_project_settings
    settings = get_project_settings()

import warnings
from pyrake.exceptions import pyrakeDeprecationWarning
warnings.warn("Module `pyrake.conf` is deprecated, use `crawler.settings` attribute instead",
    pyrakeDeprecationWarning, stacklevel=2)
