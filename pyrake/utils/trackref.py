"""

Purpose:

-Record and report references to live object instances or subclass (object_ref)

Issues:



"""

from __future__ import print_function
import weakref, os, six
from collections import defaultdict
from time import time
from operator import itemgetter

NoneType = type(None)

live_refs = defaultdict(weakref.WeakKeyDictionary)

#Function: inherit from this class not object to record live instances
class object_ref(object):

    __slots__ = ()

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        live_refs[cls][obj] = time()
        return obj

def format_live_refs(ignore=NoneType):
    s = "Live References" + os.linesep + os.linesep
    now = time()
    for cls, wdict in six.iteritems(live_refs):
        if not wdict:
            continue
        if issubclass(cls, ignore):
            continue
        oldest = min(wdict.itervalues())
        s += "%-15s %7d   oldest: %ds ago" % (cls.__name__, len(wdict), \
            now-oldest) + os.linesep
    return s

def print_live_refs(*a, **kw):
    print(format_live_refs(*a, **kw))

def get_oldest(class_name):
    for cls, wdict in six.iteritems(live_refs):
        if cls.__name__ == class_name:
            if wdict:
                return min(six.iteritems(wdict), key=itemgetter(1))[0]

def iter_all(class_name):
    for cls, wdict in six.iteritems(live_refs):
        if cls.__name__ == class_name:
            return six.iterkeys(wdict)