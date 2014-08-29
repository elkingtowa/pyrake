import os
import sys
from operator import itemgetter

import six
from six.moves.configparser import SafeConfigParser


def build_component_list(base, custom):
    """Compose a component list based on a custom and base dict of components
    (typically middlewares or extensions), unless custom is already a list, in
    which case it's returned.
    """
    if isinstance(custom, (list, tuple)):
        return custom
    compdict = base.copy()
    compdict.update(custom)
    items = (x for x in six.iteritems(compdict) if x[1] is not None)
    return [x[0] for x in sorted(items, key=itemgetter(1))]


def arglist_to_dict(arglist):
    """Convert a list of arguments like ['arg1=val1', 'arg2=val2', ...] to a
    dict
    """
    return dict(x.split('=', 1) for x in arglist)


def closest_pyrake_cfg(path='.', prevpath=None):
    """Return the path to the closest pyrake.cfg file by traversing the current
    directory and its parents
    """
    if path == prevpath:
        return ''
    path = os.path.abspath(path)
    cfgfile = os.path.join(path, 'pyrake.cfg')
    if os.path.exists(cfgfile):
        return cfgfile
    return closest_pyrake_cfg(os.path.dirname(path), path)


def init_env(project='default', set_syspath=True):
    """Initialize environment to use command-line tool from inside a project
    dir. This sets the pyrake settings module and modifies the Python path to
    be able to locate the project module.
    """
    cfg = get_config()
    if cfg.has_option('settings', project):
        os.environ['pyrake_SETTINGS_MODULE'] = cfg.get('settings', project)
    closest = closest_pyrake_cfg()
    if closest:
        projdir = os.path.dirname(closest)
        if set_syspath and projdir not in sys.path:
            sys.path.append(projdir)


def get_config(use_closest=True):
    """Get pyrake config file as a SafeConfigParser"""
    sources = get_sources(use_closest)
    cfg = SafeConfigParser()
    cfg.read(sources)
    return cfg


def get_sources(use_closest=True):
    sources = ['/etc/pyrake.cfg', r'c:\pyrake\pyrake.cfg',
               os.path.expanduser('~/.pyrake.cfg')]
    if use_closest:
        sources.append(closest_pyrake_cfg())
    return sources
