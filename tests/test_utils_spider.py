import unittest
from pyrake.http import Request
from pyrake.item import BaseItem
from pyrake.utils.spider import iterate_spider_output, iter_spider_classes

from pyrake.contrib.spiders import CrawlSpider


class MyBaseSpider(CrawlSpider):
    pass # abstract spider

class MySpider1(MyBaseSpider):
    name = 'myspider1'

class MySpider2(MyBaseSpider):
    name = 'myspider2'

class UtilsSpidersTestCase(unittest.TestCase):

    def test_iterate_spider_output(self):
        i = BaseItem()
        r = Request('http://pyraketest.org')
        o = object()

        self.assertEqual(list(iterate_spider_output(i)), [i])
        self.assertEqual(list(iterate_spider_output(r)), [r])
        self.assertEqual(list(iterate_spider_output(o)), [o])
        self.assertEqual(list(iterate_spider_output([r, i, o])), [r, i, o])

    def test_iter_spider_classes(self):
        import tests.test_utils_spider
        it = iter_spider_classes(tests.test_utils_spider)
        self.assertEqual(set(it), {MySpider1, MySpider2})

if __name__ == "__main__":
    unittest.main()
