"""
XPath selectors based on lxml
"""
from pyrake.utils.deprecate import create_deprecated_class
from .unified import Selector, SelectorList


__all__ = ['HtmlXPathSelector', 'XmlXPathSelector', 'XPathSelector',
           'XPathSelectorList']

def _xpathselector_css(self, *a, **kw):
    raise RuntimeError('.css() method not available for %s, '
                        'instantiate pyrake.Selector '
                        'instead' % type(self).__name__)

XPathSelector = create_deprecated_class(
    'XPathSelector',
    Selector,
    {
        '__slots__': (),
        '_default_type': 'html',
        'css': _xpathselector_css,
    },
    new_class_path='pyrake.Selector',
    old_class_path='pyrake.selector.XPathSelector',
)

XmlXPathSelector = create_deprecated_class(
    'XmlXPathSelector',
    XPathSelector,
    clsdict={
        '__slots__': (),
        '_default_type': 'xml',
    },
    new_class_path='pyrake.Selector',
    old_class_path='pyrake.selector.XmlXPathSelector',
)

HtmlXPathSelector = create_deprecated_class(
    'HtmlXPathSelector',
    XPathSelector,
    clsdict={
        '__slots__': (),
        '_default_type': 'html',
    },
    new_class_path='pyrake.Selector',
    old_class_path='pyrake.selector.HtmlXPathSelector',
)

XPathSelectorList = create_deprecated_class('XPathSelectorList', SelectorList)
