from unittest import TestCase

from pyrake.contrib.spidermiddleware.urllength import UrlLengthMiddleware
from pyrake.http import Response, Request
from pyrake.spider import Spider


class TestUrlLengthMiddleware(TestCase):

    def test_process_spider_output(self):
        res = Response('http://pyraketest.org')

        short_url_req = Request('http://pyraketest.org/')
        long_url_req = Request('http://pyraketest.org/this_is_a_long_url')
        reqs = [short_url_req, long_url_req]

        mw = UrlLengthMiddleware(maxlength=25)
        spider = Spider('foo')
        out = list(mw.process_spider_output(res, reqs, spider))
        self.assertEquals(out, [short_url_req])

