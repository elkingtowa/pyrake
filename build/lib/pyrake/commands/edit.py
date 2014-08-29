import sys, os

from pyrake.command import pyrakeCommand
from pyrake.exceptions import UsageError

class Command(pyrakeCommand):

    requires_project = True
    default_settings = {'LOG_ENABLED': False}

    def syntax(self):
        return "<spider>"

    def short_desc(self):
        return "Edit spider"

    def long_desc(self):
        return "Edit a spider using the editor defined in EDITOR setting"

    def _err(self, msg):
        sys.stderr.write(msg + os.linesep)
        self.exitcode = 1

    def run(self, args, opts):
        if len(args) != 1:
            raise UsageError()

        crawler = self.crawler_process.create_crawler()
        editor = crawler.settings['EDITOR']
        try:
            spider = crawler.spiders.create(args[0])
        except KeyError:
            return self._err("Spider not found: %s" % args[0])

        sfile = sys.modules[spider.__module__].__file__
        sfile = sfile.replace('.pyc', '.py')
        self.exitcode = os.system('%s "%s"' % (editor, sfile))
