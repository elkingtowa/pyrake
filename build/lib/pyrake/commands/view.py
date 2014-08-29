from pyrake.command import pyrakeCommand
from pyrake.commands import fetch
from pyrake.utils.response import open_in_browser

class Command(fetch.Command):

    def short_desc(self):
        return "Open URL in browser, as seen by pyrake"

    def long_desc(self):
        return "Fetch a URL using the pyrake downloader and show its " \
            "contents in a browser"

    def add_options(self, parser):
        pyrakeCommand.add_options(self, parser)
        parser.add_option("--spider", dest="spider",
            help="use this spider")

    def _print_response(self, response, opts):
        open_in_browser(response)
