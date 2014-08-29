import sys
import time
import subprocess

from six.moves.urllib.parse import urlencode

import pyrake
from pyrake.command import pyrakeCommand
from pyrake.contrib.linkextractors import LinkExtractor


class Command(pyrakeCommand):

    default_settings = {
        'LOG_LEVEL': 'INFO',
        'LOGSTATS_INTERVAL': 1,
        'CLOSESPIDER_TIMEOUT': 10,
    }

    def short_desc(self):
        return "Run quick benchmark test"

    def run(self, args, opts):
        with _BenchServer():
            spider = _BenchSpider(total=100000)
            crawler = self.crawler_process.create_crawler()
            crawler.crawl(spider)
            self.crawler_process.start()


class _BenchServer(object):

    def __enter__(self):
        from pyrake.utils.test import get_testenv
        pargs = [sys.executable, '-u', '-m', 'pyrake.utils.benchserver']
        self.proc = subprocess.Popen(pargs, stdout=subprocess.PIPE,
                                     env=get_testenv())
        self.proc.stdout.readline()

    def __exit__(self, exc_type, exc_value, traceback):
        self.proc.kill()
        self.proc.wait()
        time.sleep(0.2)


class _BenchSpider(pyrake.Spider):
    """A spider that follows all links"""
    name = 'follow'
    total = 10000
    show = 20
    baseurl = 'http://localhost:8998'
    link_extractor = LinkExtractor()

    def start_requests(self):
        qargs = {'total': self.total, 'show': self.show}
        url = '{}?{}'.format(self.baseurl, urlencode(qargs, doseq=1))
        return [pyrake.Request(url, dont_filter=True)]

    def parse(self, response):
        for link in self.link_extractor.extract_links(response):
            yield pyrake.Request(link.url, callback=self.parse)
