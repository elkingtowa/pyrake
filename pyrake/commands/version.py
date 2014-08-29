from __future__ import print_function
import sys
import platform

import twisted

import pyrake
from pyrake.command import pyrakeCommand


class Command(pyrakeCommand):

    def syntax(self):
        return "[-v]"

    def short_desc(self):
        return "Print pyrake version"

    def add_options(self, parser):
        pyrakeCommand.add_options(self, parser)
        parser.add_option("--verbose", "-v", dest="verbose", action="store_true",
            help="also display twisted/python/platform info (useful for bug reports)")

    def run(self, args, opts):
        if opts.verbose:
            import lxml.etree
            lxml_version = ".".join(map(str, lxml.etree.LXML_VERSION))
            libxml2_version = ".".join(map(str, lxml.etree.LIBXML_VERSION))
            print("pyrake  : %s" % pyrake.__version__)
            print("lxml    : %s" % lxml_version)
            print("libxml2 : %s" % libxml2_version)
            print("Twisted : %s" % twisted.version.short())
            print("Python  : %s" % sys.version.replace("\n", "- "))
            print("Platform: %s" % platform.platform())
        else:
            print("pyrake %s" % pyrake.__version__)
