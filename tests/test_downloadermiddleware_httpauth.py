import unittest

from pyrake.http import Request
from pyrake.contrib.downloadermiddleware.httpauth import HttpAuthMiddleware
from pyrake.spider import Spider

class TestSpider(Spider):
    http_user = 'foo'
    http_pass = 'bar'

class HttpAuthMiddlewareTest(unittest.TestCase):

    def setUp(self):
        self.mw = HttpAuthMiddleware()
        self.spider = TestSpider('foo')
        self.mw.spider_opened(self.spider)

    def tearDown(self):
        del self.mw

    def test_auth(self):
        req = Request('http://pyraketest.org/')
        assert self.mw.process_request(req, self.spider) is None
        self.assertEquals(req.headers['Authorization'], 'Basic Zm9vOmJhcg==')

    def test_auth_already_set(self):
        req = Request('http://pyraketest.org/', headers=dict(Authorization='Digest 123'))
        assert self.mw.process_request(req, self.spider) is None
        self.assertEquals(req.headers['Authorization'], 'Digest 123')


if __name__ == '__main__':
    unittest.main()
