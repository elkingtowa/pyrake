import os                
import shutil
import click
from pkg_resources import safe_name

class Repo(object):

    def __init__(self):
        self.home = os.path.expanduser('~/.local/venvs')
        self.bin_dir = os.path.expanduser('~/.local/bin')

    def get_package_path(self, package):
        return os.path.join(self.home, normalize_package(package))

    def find_installed_executables(self, path):
        prefix = os.path.realpath(os.path.normpath(path)) + '/'
        try:
            for filename in os.listdir(self.bin_dir):
                exe = os.path.join(self.bin_dir, filename)
                target = real_readlink(exe)
                if target is None:
                    continue
                if target.startswith(prefix):
                    yield exe
        except OSError:
            pass

    def find_scripts(self, virtualenv, package):
        prefix = os.path.normpath(os.path.realpath(os.path.join(
            virtualenv, 'bin'))) + '/'

        from subprocess import Popen, PIPE
        files = Popen([prefix + 'python', '-c', '''if 1:
            import os
            import pkg_resources

            dist = pkg_resources.get_distribution(%(pkg)r)
            if dist.has_metadata('RECORD'):
                for line in dist.get_metadata_lines('RECORD'):
                    print(line.split(',')[0])
            else:
                for line in dist.get_metadata_lines('installed-files.txt'):
                    print(os.path.join(dist.egg_info, line.split(',')[0]))
        ''' % {'pkg': package}], stdout=PIPE).communicate()[0].splitlines()

        for filename in files:
            filename = os.path.normpath(os.path.realpath(filename))
            if os.path.isfile(filename) and \
               filename.startswith(prefix) and \
               os.access(filename, os.X_OK):
                yield filename

    def link_scripts(self, scripts):
        rv = []
        for script in scripts:
            script_dst = os.path.join(
                self.bin_dir, os.path.basename(script))
            old_target = real_readlink(script_dst)
            if old_target == script:
                continue
            try:
                os.remove(script_dst)
            except OSError:
                pass
            try:
                os.symlink(script, script_dst)
            except OSError:
                pass
            else:
                click.echo('  Linked script %s' % script_dst)
                rv.append((script, script_dst))

        return rv

    def install(self, package, python=None):
        venv_path = self.get_package_path(package)
        if os.path.isdir(venv_path):
            click.echo('%s is already installed' % package)
            return

        from subprocess import Popen

        def _cleanup():
            try:
                shutil.rmtree(venv_path)
            except (OSError, IOError):
                pass
            return False

        # Install virtualenv
        args = ['virtualenv']
        if python is not None:
            args.append('-p')
            args.append(python)
        args.append(venv_path)
        if Popen(args).wait() != 0:
            click.echo('Failed to create virtualenv.  Aborting.')
            return _cleanup()

        if Popen([os.path.join(venv_path, 'bin', 'pip'),
                  'install', package]).wait() != 0:
            click.echo('Failed to pip install.  Aborting.')
            return _cleanup()

        # Find all the scripts
        scripts = self.find_scripts(venv_path, package)

        # And link them
        linked_scripts = self.link_scripts(scripts)

        # We did not link any, rollback.
        if not linked_scripts:
            click.echo('Did not find any scripts.  Uninstalling.')
            return _cleanup()
        return True

    def uninstall(self, package):
        path = self.get_package_path(package)
        if not os.path.isdir(path):
            return UninstallInfo(package, installed=False)
        paths = [path]
        paths.extend(self.find_installed_executables(path))
        return UninstallInfo(package, paths)

    def upgrade(self, package):
        venv_path = self.get_package_path(package)
        if not os.path.isdir(venv_path):
            click.echo('%s is not installed' % package)
            return

        from subprocess import Popen

        old_scripts = set(self.find_scripts(venv_path, package))

        if Popen([os.path.join(venv_path, 'bin', 'pip'),
                  'install', '--upgrade', package]).wait() != 0:
            click.echo('Failed to upgrade through pip.  Aborting.')
            return

        scripts = self.find_scripts(venv_path, package)
        linked_scripts = self.link_scripts(scripts)
        to_delete = old_scripts - set(x[0] for x in linked_scripts)

        for script_src, script_link in linked_scripts:
            if script_src in to_delete:
                try:
                    click.echo('  Removing old script %s' % script_src)
                    os.remove(script_link)
                except (IOError, OSError):
                    pass

    def list_everything(self):
        venvs = {}

        for venv in os.listdir(self.home):
            venv_path = os.path.join(self.home, venv)
            if os.path.isdir(venv_path) and \
               os.path.isfile(venv_path + '/bin/python'):
                venvs[venv] = []

        def _find_venv(target):
            for venv in venvs:
                if target.startswith(os.path.join(self.home, venv) + '/'):
                    return venv

        for script in os.listdir(self.bin_dir):
            exe = os.path.join(self.bin_dir, script)
            target = real_readlink(exe)
            if target is None:
                continue
            venv = _find_venv(target)
            if venv is not None:
                venvs[venv].append(script)

        return sorted(venvs.items())