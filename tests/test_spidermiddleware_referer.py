from unittest import TestCase

from pyrake.http import Response, Request
from pyrake.spider import Spider
from pyrake.contrib.spidermiddleware.referer import RefererMiddleware


class TestRefererMiddleware(TestCase):

    def setUp(self):
        self.spider = Spider('foo')
        self.mw = RefererMiddleware()

    def test_process_spider_output(self):
        res = Response('http://pyraketest.org')
        reqs = [Request('http://pyraketest.org/')]

        out = list(self.mw.process_spider_output(res, reqs, self.spider))
        self.assertEquals(out[0].headers.get('Referer'),
                          'http://pyraketest.org')

