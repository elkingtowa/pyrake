import os
from six.moves import cPickle as pickle
import warnings

from importlib import import_module
from os.path import join, dirname, abspath, isabs, exists

from pyrake.utils.conf import closest_pyrake_cfg, get_config, init_env
from pyrake.settings import Settings
from pyrake.exceptions import NotConfigured

ENVVAR = 'pyrake_SETTINGS_MODULE'
DATADIR_CFG_SECTION = 'datadir'

def inside_project():
    pyrake_module = os.environ.get('pyrake_SETTINGS_MODULE')
    if pyrake_module is not None:
        try:
            import_module(pyrake_module)
        except ImportError as exc:
            warnings.warn("Cannot import pyrake settings module %s: %s" % (pyrake_module, exc))
        else:
            return True
    return bool(closest_pyrake_cfg())

def project_data_dir(project='default'):
    """Return the current project data dir, creating it if it doesn't exist"""
    if not inside_project():
        raise NotConfigured("Not inside a project")
    cfg = get_config()
    if cfg.has_option(DATADIR_CFG_SECTION, project):
        d = cfg.get(DATADIR_CFG_SECTION, project)
    else:
        pyrake_cfg = closest_pyrake_cfg()
        if not pyrake_cfg:
            raise NotConfigured("Unable to find pyrake.cfg file to infer project data dir")
        d = abspath(join(dirname(pyrake_cfg), '.pyrake'))
    if not exists(d):
        os.makedirs(d)
    return d

def data_path(path, createdir=False):
    """If path is relative, return the given path inside the project data dir,
    otherwise return the path unmodified
    """
    if not isabs(path):
        path = join(project_data_dir(), path)
    if createdir and not exists(path):
        os.makedirs(path)
    return path

def get_project_settings():
    if ENVVAR not in os.environ:
        project = os.environ.get('pyrake_PROJECT', 'default')
        init_env(project)

    settings = Settings()
    settings_module_path = os.environ.get(ENVVAR)
    if settings_module_path:
        settings.setmodule(settings_module_path, priority='project')

    # XXX: remove this hack
    pickled_settings = os.environ.get("pyrake_PICKLED_SETTINGS_TO_OVERRIDE")
    if pickled_settings:
        settings.setdict(pickle.loads(pickled_settings), priority='project')

    # XXX: deprecate and remove this functionality
    env_overrides = {k[7:]: v for k, v in os.environ.items() if
                     k.startswith('pyrake_')}
    if env_overrides:
        settings.setdict(env_overrides, priority='project')

    return settings
