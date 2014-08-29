import unittest
from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, \
        ConnectionRefusedError, ConnectionDone, ConnectError, \
        ConnectionLost, TCPTimedOutError

from pyrake import optional_features
from pyrake.contrib.downloadermiddleware.retry import RetryMiddleware
from pyrake.xlib.tx import ResponseFailed
from pyrake.spider import Spider
from pyrake.http import Request, Response
from pyrake.utils.test import get_crawler


class RetryTest(unittest.TestCase):
    def setUp(self):
        crawler = get_crawler()
        self.spider = Spider('foo')
        self.mw = RetryMiddleware.from_crawler(crawler)
        self.mw.max_retry_times = 2

    def test_priority_adjust(self):
        req = Request('http://www.pyraketest.org/503')
        rsp = Response('http://www.pyraketest.org/503', body='', status=503)
        req2 = self.mw.process_response(req, rsp, self.spider)
        assert req2.priority < req.priority

    def test_404(self):
        req = Request('http://www.pyraketest.org/404')
        rsp = Response('http://www.pyraketest.org/404', body='', status=404)

        # dont retry 404s
        assert self.mw.process_response(req, rsp, self.spider) is rsp

    def test_dont_retry(self):
        req = Request('http://www.pyraketest.org/503', meta={'dont_retry': True})
        rsp = Response('http://www.pyraketest.org/503', body='', status=503)

        # first retry
        r = self.mw.process_response(req, rsp, self.spider)
        assert r is rsp

        # Test retry when dont_retry set to False
        req = Request('http://www.pyraketest.org/503', meta={'dont_retry': False})
        rsp = Response('http://www.pyraketest.org/503')

        # first retry
        r = self.mw.process_response(req, rsp, self.spider)
        assert r is rsp

    def test_dont_retry_exc(self):
        req = Request('http://www.pyraketest.org/503', meta={'dont_retry': True})

        r = self.mw.process_exception(req, DNSLookupError(), self.spider)
        assert r is None

    def test_503(self):
        req = Request('http://www.pyraketest.org/503')
        rsp = Response('http://www.pyraketest.org/503', body='', status=503)

        # first retry
        req = self.mw.process_response(req, rsp, self.spider)
        assert isinstance(req, Request)
        self.assertEqual(req.meta['retry_times'], 1)

        # second retry
        req = self.mw.process_response(req, rsp, self.spider)
        assert isinstance(req, Request)
        self.assertEqual(req.meta['retry_times'], 2)

        # discard it
        assert self.mw.process_response(req, rsp, self.spider) is rsp

    def test_twistederrors(self):
        exceptions = [defer.TimeoutError, TCPTimedOutError, TimeoutError,
                DNSLookupError, ConnectionRefusedError, ConnectionDone,
                ConnectError, ConnectionLost]
        if 'http11' in optional_features:
            exceptions.append(ResponseFailed)

        for exc in exceptions:
            req = Request('http://www.pyraketest.org/%s' % exc.__name__)
            self._test_retry_exception(req, exc('foo'))

    def _test_retry_exception(self, req, exception):
        # first retry
        req = self.mw.process_exception(req, exception, self.spider)
        assert isinstance(req, Request)
        self.assertEqual(req.meta['retry_times'], 1)

        # second retry
        req = self.mw.process_exception(req, exception, self.spider)
        assert isinstance(req, Request)
        self.assertEqual(req.meta['retry_times'], 2)

        # discard it
        req = self.mw.process_exception(req, exception, self.spider)
        self.assertEqual(req, None)


if __name__ == "__main__":
    unittest.main()