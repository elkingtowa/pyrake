from twisted.trial import unittest
from twisted.internet import defer

from pyrake.utils.testsite import SiteTest
from pyrake.utils.testproc import ProcessTest


class FetchTest(ProcessTest, SiteTest, unittest.TestCase):

    command = 'fetch'

    @defer.inlineCallbacks
    def test_output(self):
        _, out, _ = yield self.execute([self.url('/text')])
        self.assertEqual(out.strip(), 'Works')

    @defer.inlineCallbacks
    def test_headers(self):
        _, out, _ = yield self.execute([self.url('/text'), '--headers'])
        out = out.replace('\r', '') # required on win32
        assert 'Server: TwistedWeb' in out
        assert 'Content-Type: text/plain' in out
