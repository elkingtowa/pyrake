from unittest import TestCase

from six.moves.urllib.parse import urlparse

from pyrake.http import Response, Request
from pyrake.spider import Spider
from pyrake.contrib.spidermiddleware.offsite import OffsiteMiddleware
from pyrake.utils.test import get_crawler

class TestOffsiteMiddleware(TestCase):

    def setUp(self):
        self.spider = self._get_spider()
        crawler = get_crawler()
        self.mw = OffsiteMiddleware.from_crawler(crawler)
        self.mw.spider_opened(self.spider)

    def _get_spider(self):
        return Spider('foo', allowed_domains=['pyraketest.org', 'pyrake.org'])

    def test_process_spider_output(self):
        res = Response('http://pyraketest.org')

        onsite_reqs = [Request('http://pyraketest.org/1'),
                       Request('http://pyrake.org/1'),
                       Request('http://sub.pyrake.org/1'),
                       Request('http://offsite.tld/letmepass', dont_filter=True)]
        offsite_reqs = [Request('http://pyrake2.org'),
                       Request('http://offsite.tld/'),
                       Request('http://offsite.tld/pyraketest.org'),
                       Request('http://offsite.tld/rogue.pyraketest.org'),
                       Request('http://rogue.pyraketest.org.haha.com'),
                       Request('http://roguepyraketest.org')]
        reqs = onsite_reqs + offsite_reqs

        out = list(self.mw.process_spider_output(res, reqs, self.spider))
        self.assertEquals(out, onsite_reqs)


class TestOffsiteMiddleware2(TestOffsiteMiddleware):

    def _get_spider(self):
        return Spider('foo', allowed_domains=None)

    def test_process_spider_output(self):
        res = Response('http://pyraketest.org')
        reqs = [Request('http://a.com/b.html'), Request('http://b.com/1')]
        out = list(self.mw.process_spider_output(res, reqs, self.spider))
        self.assertEquals(out, reqs)

class TestOffsiteMiddleware3(TestOffsiteMiddleware2):

    def _get_spider(self):
        return Spider('foo')


class TestOffsiteMiddleware4(TestOffsiteMiddleware3):

    def _get_spider(self):
      bad_hostname = urlparse('http:////pyraketest.org').hostname
      return Spider('foo', allowed_domains=['pyraketest.org', None, bad_hostname])

    def test_process_spider_output(self):
      res = Response('http://pyraketest.org')
      reqs = [Request('http://pyraketest.org/1')]
      out = list(self.mw.process_spider_output(res, reqs, self.spider))
      self.assertEquals(out, reqs)
