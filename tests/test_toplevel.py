from unittest import TestCase
import six
import pyrake


class ToplevelTestCase(TestCase):

    def test_version(self):
        self.assertIs(type(pyrake.__version__), six.text_type)

    def test_version_info(self):
        self.assertIs(type(pyrake.version_info), tuple)

    def test_optional_features(self):
        self.assertIs(type(pyrake.optional_features), set)
        self.assertIn('ssl', pyrake.optional_features)

    def test_request_shortcut(self):
        from pyrake.http import Request, FormRequest
        self.assertIs(pyrake.Request, Request)
        self.assertIs(pyrake.FormRequest, FormRequest)

    def test_spider_shortcut(self):
        from pyrake.spider import Spider
        self.assertIs(pyrake.Spider, Spider)

    def test_selector_shortcut(self):
        from pyrake.selector import Selector
        self.assertIs(pyrake.Selector, Selector)

    def test_item_shortcut(self):
        from pyrake.item import Item, Field
        self.assertIs(pyrake.Item, Item)
        self.assertIs(pyrake.Field, Field)
