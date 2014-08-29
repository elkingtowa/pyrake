from unittest import TestCase

from pyrake.contrib.spidermiddleware.depth import DepthMiddleware
from pyrake.http import Response, Request
from pyrake.spider import Spider
from pyrake.statscol import StatsCollector
from pyrake.utils.test import get_crawler


class TestDepthMiddleware(TestCase):

    def setUp(self):
        self.spider = Spider('pyraketest.org')

        self.stats = StatsCollector(get_crawler())
        self.stats.open_spider(self.spider)

        self.mw = DepthMiddleware(1, self.stats, True)

    def test_process_spider_output(self):
        req = Request('http://pyraketest.org')
        resp = Response('http://pyraketest.org')
        resp.request = req
        result = [Request('http://pyraketest.org')]

        out = list(self.mw.process_spider_output(resp, result, self.spider))
        self.assertEquals(out, result)

        rdc = self.stats.get_value('request_depth_count/1', spider=self.spider)
        self.assertEquals(rdc, 1)

        req.meta['depth'] = 1

        out2 = list(self.mw.process_spider_output(resp, result, self.spider))
        self.assertEquals(out2, [])

        rdm = self.stats.get_value('request_depth_max', spider=self.spider)
        self.assertEquals(rdm, 1)
 
    def tearDown(self):
        self.stats.close_spider(self.spider, '')

