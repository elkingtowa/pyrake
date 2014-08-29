import warnings
from pyrake.exceptions import pyrakeDeprecationWarning
warnings.warn("Module `pyrake.contrib_exp.djangoitem` is deprecated, use `pyrake.contrib.djangoitem` instead",
    pyrakeDeprecationWarning, stacklevel=2)

from pyrake.contrib.djangoitem import DjangoItem
