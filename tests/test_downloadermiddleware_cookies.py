from unittest import TestCase
import re

from pyrake.http import Response, Request
from pyrake.spider import Spider
from pyrake.contrib.downloadermiddleware.cookies import CookiesMiddleware


class CookiesMiddlewareTest(TestCase):

    def assertCookieValEqual(self, first, second, msg=None):
        cookievaleq = lambda cv: re.split(';\s*', cv)
        return self.assertEqual(
            sorted(cookievaleq(first)),
            sorted(cookievaleq(second)), msg)

    def setUp(self):
        self.spider = Spider('foo')
        self.mw = CookiesMiddleware()

    def tearDown(self):
        del self.mw

    def test_basic(self):
        headers = {'Set-Cookie': 'C1=value1; path=/'}
        req = Request('http://pyraketest.org/')
        assert self.mw.process_request(req, self.spider) is None
        assert 'Cookie' not in req.headers

        res = Response('http://pyraketest.org/', headers=headers)
        assert self.mw.process_response(req, res, self.spider) is res

        #assert res.cookies

        req2 = Request('http://pyraketest.org/sub1/')
        assert self.mw.process_request(req2, self.spider) is None
        self.assertEquals(req2.headers.get('Cookie'), "C1=value1")

    def test_dont_merge_cookies(self):
        # merge some cookies into jar
        headers = {'Set-Cookie': 'C1=value1; path=/'}
        req = Request('http://pyraketest.org/')
        res = Response('http://pyraketest.org/', headers=headers)
        assert self.mw.process_response(req, res, self.spider) is res

        # test Cookie header is not seted to request
        req = Request('http://pyraketest.org/dontmerge', meta={'dont_merge_cookies': 1})
        assert self.mw.process_request(req, self.spider) is None
        assert 'Cookie' not in req.headers

        # check that returned cookies are not merged back to jar
        res = Response('http://pyraketest.org/dontmerge', headers={'Set-Cookie': 'dont=mergeme; path=/'})
        assert self.mw.process_response(req, res, self.spider) is res

        # check that cookies are merged back
        req = Request('http://pyraketest.org/mergeme')
        assert self.mw.process_request(req, self.spider) is None
        self.assertEquals(req.headers.get('Cookie'), 'C1=value1')

        # check that cookies are merged when dont_merge_cookies is passed as 0
        req = Request('http://pyraketest.org/mergeme', meta={'dont_merge_cookies': 0})
        assert self.mw.process_request(req, self.spider) is None
        self.assertEquals(req.headers.get('Cookie'), 'C1=value1')

    def test_complex_cookies(self):
        # merge some cookies into jar
        cookies = [{'name': 'C1', 'value': 'value1', 'path': '/foo', 'domain': 'pyraketest.org'},
                {'name': 'C2', 'value': 'value2', 'path': '/bar', 'domain': 'pyraketest.org'},
                {'name': 'C3', 'value': 'value3', 'path': '/foo', 'domain': 'pyraketest.org'},
                {'name': 'C4', 'value': 'value4', 'path': '/foo', 'domain': 'pyrake.org'}]


        req = Request('http://pyraketest.org/', cookies=cookies)
        self.mw.process_request(req, self.spider)

        # embed C1 and C3 for pyraketest.org/foo
        req = Request('http://pyraketest.org/foo')
        self.mw.process_request(req, self.spider)
        assert req.headers.get('Cookie') in ('C1=value1; C3=value3', 'C3=value3; C1=value1')

        # embed C2 for pyraketest.org/bar
        req = Request('http://pyraketest.org/bar')
        self.mw.process_request(req, self.spider)
        self.assertEquals(req.headers.get('Cookie'), 'C2=value2')

        # embed nothing for pyraketest.org/baz
        req = Request('http://pyraketest.org/baz')
        self.mw.process_request(req, self.spider)
        assert 'Cookie' not in req.headers

    def test_merge_request_cookies(self):
        req = Request('http://pyraketest.org/', cookies={'galleta': 'salada'})
        assert self.mw.process_request(req, self.spider) is None
        self.assertEquals(req.headers.get('Cookie'), 'galleta=salada')

        headers = {'Set-Cookie': 'C1=value1; path=/'}
        res = Response('http://pyraketest.org/', headers=headers)
        assert self.mw.process_response(req, res, self.spider) is res

        req2 = Request('http://pyraketest.org/sub1/')
        assert self.mw.process_request(req2, self.spider) is None

        self.assertCookieValEqual(req2.headers.get('Cookie'), "C1=value1; galleta=salada")

    def test_cookiejar_key(self):
        req = Request('http://pyraketest.org/', cookies={'galleta': 'salada'}, meta={'cookiejar': "store1"})
        assert self.mw.process_request(req, self.spider) is None
        self.assertEquals(req.headers.get('Cookie'), 'galleta=salada')

        headers = {'Set-Cookie': 'C1=value1; path=/'}
        res = Response('http://pyraketest.org/', headers=headers, request=req)
        assert self.mw.process_response(req, res, self.spider) is res

        req2 = Request('http://pyraketest.org/', meta=res.meta)
        assert self.mw.process_request(req2, self.spider) is None
        self.assertCookieValEqual(req2.headers.get('Cookie'),'C1=value1; galleta=salada')

        req3 = Request('http://pyraketest.org/', cookies={'galleta': 'dulce'}, meta={'cookiejar': "store2"})
        assert self.mw.process_request(req3, self.spider) is None
        self.assertEquals(req3.headers.get('Cookie'), 'galleta=dulce')

        headers = {'Set-Cookie': 'C2=value2; path=/'}
        res2 = Response('http://pyraketest.org/', headers=headers, request=req3)
        assert self.mw.process_response(req3, res2, self.spider) is res2

        req4 = Request('http://pyraketest.org/', meta=res2.meta)
        assert self.mw.process_request(req4, self.spider) is None
        self.assertCookieValEqual(req4.headers.get('Cookie'), 'C2=value2; galleta=dulce')

        #cookies from hosts with port
        req5_1 = Request('http://pyraketest.org:1104/')
        assert self.mw.process_request(req5_1, self.spider) is None

        headers = {'Set-Cookie': 'C1=value1; path=/'}
        res5_1 = Response('http://pyraketest.org:1104/', headers=headers, request=req5_1)
        assert self.mw.process_response(req5_1, res5_1, self.spider) is res5_1

        req5_2 = Request('http://pyraketest.org:1104/some-redirected-path')
        assert self.mw.process_request(req5_2, self.spider) is None
        self.assertEquals(req5_2.headers.get('Cookie'), 'C1=value1')

        req5_3 = Request('http://pyraketest.org/some-redirected-path')
        assert self.mw.process_request(req5_3, self.spider) is None
        self.assertEquals(req5_3.headers.get('Cookie'), 'C1=value1')

        #skip cookie retrieval for not http request
        req6 = Request('file:///pyrake/sometempfile')
        assert self.mw.process_request(req6, self.spider) is None
        self.assertEquals(req6.headers.get('Cookie'), None)
