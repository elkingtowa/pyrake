from __future__ import print_function
from pyrake.command import pyrakeCommand

class Command(pyrakeCommand):

    requires_project = True
    default_settings = {'LOG_ENABLED': False}

    def short_desc(self):
        return "List available spiders"

    def run(self, args, opts):
        crawler = self.crawler_process.create_crawler()
        for s in sorted(crawler.spiders.list()):
            print(s)
