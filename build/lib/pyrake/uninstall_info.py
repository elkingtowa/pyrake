import os

class UninstallInfo(object):

    def __init__(self, package, paths=None, installed=True):
        self.package = package
        self.paths = paths or []
        self.installed = installed

    def perform(self):
        for path in self.paths:
            try:
                os.remove(path)
            except OSError:
                shutil.rmtree(path)