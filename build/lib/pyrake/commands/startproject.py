from __future__ import print_function
import re
import shutil
import string
from importlib import import_module
from os.path import join, exists, abspath
from shutil import copytree, ignore_patterns

import pyrake
from pyrake.command import pyrakeCommand
from pyrake.utils.template import render_templatefile, string_camelcase
from pyrake.exceptions import UsageError


TEMPLATES_PATH = join(pyrake.__path__[0], 'templates', 'project')

TEMPLATES_TO_RENDER = (
    ('pyrake.cfg',),
    ('${project_name}', 'settings.py.tmpl'),
    ('${project_name}', 'items.py.tmpl'),
    ('${project_name}', 'pipelines.py.tmpl'),
)

IGNORE = ignore_patterns('*.pyc', '.svn')


class Command(pyrakeCommand):

    requires_project = False

    def syntax(self):
        return "<project_name>"

    def short_desc(self):
        return "Create new project"

    def _is_valid_name(self, project_name):
        def _module_exists(module_name):
            try:
                import_module(module_name)
                return True
            except ImportError:
                return False

        if not re.search(r'^[_a-zA-Z]\w*$', project_name):
            print('Error: Project names must begin with a letter and contain'\
                    ' only\nletters, numbers and underscores')
        elif exists(project_name):
            print('Error: Directory %r already exists' % project_name)
        elif _module_exists(project_name):
            print('Error: Module %r already exists' % project_name)
        else:
            return True
        return False

    def run(self, args, opts):
        if len(args) != 1:
            raise UsageError()
        project_name = args[0]

        if not self._is_valid_name(project_name):
            self.exitcode = 1
            return

        moduletpl = join(TEMPLATES_PATH, 'module')
        copytree(moduletpl, join(project_name, project_name), ignore=IGNORE)
        shutil.copy(join(TEMPLATES_PATH, 'pyrake.cfg'), project_name)
        for paths in TEMPLATES_TO_RENDER:
            path = join(*paths)
            tplfile = join(project_name,
                string.Template(path).substitute(project_name=project_name))
            render_templatefile(tplfile, project_name=project_name,
                ProjectName=string_camelcase(project_name))
        print("New pyrake project %r created in:" % project_name)
        print("    %s\n" % abspath(project_name))
        print("You can start your first spider with:")
        print("    cd %s" % project_name)
        print("    pyrake genspider example example.com")
