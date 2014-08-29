.. _topics-extensions:

==========
Extensions
==========

The extensions framework provides a mechanism for inserting your own
custom functionality into pyrake. 

Extensions are just regular classes that are instantiated at pyrake startup,
when extensions are initialized.

Extension settings
==================

Extensions use the :ref:`pyrake settings <topics-settings>` to manage their
settings, just like any other pyrake code.

It is customary for extensions to prefix their settings with their own name, to
avoid collision with existing (and future) extensions. For example, an
hypothetic extension to handle `Google Sitemaps`_ would use settings like
`GOOGLESITEMAP_ENABLED`, `GOOGLESITEMAP_DEPTH`, and so on.

.. _Google Sitemaps: http://en.wikipedia.org/wiki/Sitemaps

Loading & activating extensions
===============================

Extensions are loaded and activated at startup by instantiating a single
instance of the extension class. Therefore, all the extension initialization
code must be performed in the class constructor (``__init__`` method).

To make an extension available, add it to the :setting:`EXTENSIONS` setting in
your pyrake settings. In :setting:`EXTENSIONS`, each extension is represented
by a string: the full Python path to the extension's class name. For example::

    EXTENSIONS = {
        'pyrake.contrib.corestats.CoreStats': 500,
        'pyrake.telnet.TelnetConsole': 500,
    }


As you can see, the :setting:`EXTENSIONS` setting is a dict where the keys are
the extension paths, and their values are the orders, which define the
extension *loading* order. Extensions orders are not as important as middleware
orders though, and they are typically irrelevant, ie. it doesn't matter in
which order the extensions are loaded because they don't depend on each other
[1].

However, this feature can be exploited if you need to add an extension which
depends on other extensions already loaded.

[1] This is is why the :setting:`EXTENSIONS_BASE` setting in pyrake (which
contains all built-in extensions enabled by default) defines all the extensions
with the same order (``500``).

Available, enabled and disabled extensions
==========================================

Not all available extensions will be enabled. Some of them usually depend on a
particular setting. For example, the HTTP Cache extension is available by default
but disabled unless the :setting:`HTTPCACHE_ENABLED` setting is set.

Disabling an extension
======================

In order to disable an extension that comes enabled by default (ie. those
included in the :setting:`EXTENSIONS_BASE` setting) you must set its order to
``None``. For example::

    EXTENSIONS = {
        'pyrake.contrib.corestats.CoreStats': None,
    }

Writing your own extension
==========================

Writing your own extension is easy. Each extension is a single Python class
which doesn't need to implement any particular method. 

The main entry point for a pyrake extension (this also includes middlewares and
pipelines) is the ``from_crawler`` class method which receives a
``Crawler`` instance which is the main object controlling the pyrake crawler.
Through that object you can access settings, signals, stats, and also control
the crawler behaviour, if your extension needs to such thing.

Typically, extensions connect to :ref:`signals <topics-signals>` and perform
tasks triggered by them.

Finally, if the ``from_crawler`` method raises the
:exc:`~pyrake.exceptions.NotConfigured` exception, the extension will be
disabled. Otherwise, the extension will be enabled.

Sample extension
----------------

Here we will implement a simple extension to illustrate the concepts described
in the previous section. This extension will log a message every time:

* a spider is opened
* a spider is closed
* a specific number of items are scraped

The extension will be enabled through the ``MYEXT_ENABLED`` setting and the
number of items will be specified through the ``MYEXT_ITEMCOUNT`` setting.

Here is the code of such extension::

    from pyrake import signals
    from pyrake.exceptions import NotConfigured

    class SpiderOpenCloseLogging(object):

        def __init__(self, item_count):
            self.item_count = item_count
            self.items_scraped = 0

        @classmethod
        def from_crawler(cls, crawler):
            # first check if the extension should be enabled and raise
            # NotConfigured otherwise
            if not crawler.settings.getbool('MYEXT_ENABLED'):
                raise NotConfigured

            # get the number of items from settings
            item_count = crawler.settings.getint('MYEXT_ITEMCOUNT', 1000)

            # instantiate the extension object
            ext = cls(item_count)

            # connect the extension object to signals
            crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
            crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
            crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)

            # return the extension object 
            return ext

        def spider_opened(self, spider):
            spider.log("opened spider %s" % spider.name)

        def spider_closed(self, spider):
            spider.log("closed spider %s" % spider.name)

        def item_scraped(self, item, spider):
            self.items_scraped += 1
            if self.items_scraped == self.item_count:
                spider.log("scraped %d items, resetting counter" % self.items_scraped)
                self.item_count = 0

.. _topics-extensions-ref:

Built-in extensions reference
=============================

General purpose extensions
--------------------------

Log Stats extension
~~~~~~~~~~~~~~~~~~~

.. module:: pyrake.contrib.logstats
   :synopsis: Basic stats logging

.. class:: LogStats

Log basic stats like crawled pages and scraped items.

Core Stats extension
~~~~~~~~~~~~~~~~~~~~

.. module:: pyrake.contrib.corestats
   :synopsis: Core stats collection

.. class:: CoreStats

Enable the collection of core statistics, provided the stats collection is
enabled (see :ref:`topics-stats`).

.. _topics-extensions-ref-telnetconsole:

Telnet console extension
~~~~~~~~~~~~~~~~~~~~~~~~

.. module:: pyrake.telnet
   :synopsis: Telnet console 

.. class:: pyrake.telnet.TelnetConsole

Provides a telnet console for getting into a Python interpreter inside the
currently running pyrake process, which can be very useful for debugging. 

The telnet console must be enabled by the :setting:`TELNETCONSOLE_ENABLED`
setting, and the server will listen in the port specified in
:setting:`TELNETCONSOLE_PORT`.

.. _topics-extensions-ref-memusage:

Memory usage extension
~~~~~~~~~~~~~~~~~~~~~~

.. module:: pyrake.contrib.memusage
   :synopsis: Memory usage extension

.. class:: pyrake.contrib.memusage.MemoryUsage

.. note:: This extension does not work in Windows.

Monitors the memory used by the pyrake process that runs the spider and:

1, sends a notification e-mail when it exceeds a certain value
2. closes the spider when it exceeds a certain value

The notification e-mails can be triggered when a certain warning value is
reached (:setting:`MEMUSAGE_WARNING_MB`) and when the maximum value is reached
(:setting:`MEMUSAGE_LIMIT_MB`) which will also cause the spider to be closed
and the pyrake process to be terminated.

This extension is enabled by the :setting:`MEMUSAGE_ENABLED` setting and
can be configured with the following settings:

* :setting:`MEMUSAGE_LIMIT_MB`
* :setting:`MEMUSAGE_WARNING_MB`
* :setting:`MEMUSAGE_NOTIFY_MAIL`
* :setting:`MEMUSAGE_REPORT`

Memory debugger extension
~~~~~~~~~~~~~~~~~~~~~~~~~

.. module:: pyrake.contrib.memdebug
   :synopsis: Memory debugger extension

.. class:: pyrake.contrib.memdebug.MemoryDebugger

An extension for debugging memory usage. It collects information about:

* objects uncollected by the Python garbage collector
* objects left alive that shouldn't. For more info, see :ref:`topics-leaks-trackrefs`

To enable this extension, turn on the :setting:`MEMDEBUG_ENABLED` setting. The
info will be stored in the stats.

Close spider extension
~~~~~~~~~~~~~~~~~~~~~~

.. module:: pyrake.contrib.closespider
   :synopsis: Close spider extension

.. class:: pyrake.contrib.closespider.CloseSpider

Closes a spider automatically when some conditions are met, using a specific
closing reason for each condition.

The conditions for closing a spider can be configured through the following
settings:

* :setting:`CLOSESPIDER_TIMEOUT`
* :setting:`CLOSESPIDER_ITEMCOUNT`
* :setting:`CLOSESPIDER_PAGECOUNT`
* :setting:`CLOSESPIDER_ERRORCOUNT`

.. setting:: CLOSESPIDER_TIMEOUT

CLOSESPIDER_TIMEOUT
"""""""""""""""""""

Default: ``0``

An integer which specifies a number of seconds. If the spider remains open for
more than that number of second, it will be automatically closed with the
reason ``closespider_timeout``. If zero (or non set), spiders won't be closed by
timeout.

.. setting:: CLOSESPIDER_ITEMCOUNT

CLOSESPIDER_ITEMCOUNT
"""""""""""""""""""""

Default: ``0``

An integer which specifies a number of items. If the spider scrapes more than
that amount if items and those items are passed by the item pipeline, the
spider will be closed with the reason ``closespider_itemcount``. If zero (or
non set), spiders won't be closed by number of passed items.

.. setting:: CLOSESPIDER_PAGECOUNT

CLOSESPIDER_PAGECOUNT
"""""""""""""""""""""

.. versionadded:: 0.11

Default: ``0``

An integer which specifies the maximum number of responses to crawl. If the spider
crawls more than that, the spider will be closed with the reason
``closespider_pagecount``. If zero (or non set), spiders won't be closed by
number of crawled responses.

.. setting:: CLOSESPIDER_ERRORCOUNT

CLOSESPIDER_ERRORCOUNT
""""""""""""""""""""""

.. versionadded:: 0.11

Default: ``0``

An integer which specifies the maximum number of errors to receive before
closing the spider. If the spider generates more than that number of errors,
it will be closed with the reason ``closespider_errorcount``. If zero (or non
set), spiders won't be closed by number of errors.

StatsMailer extension
~~~~~~~~~~~~~~~~~~~~~

.. module:: pyrake.contrib.statsmailer
   :synopsis: StatsMailer extension

.. class:: pyrake.contrib.statsmailer.StatsMailer

This simple extension can be used to send a notification e-mail every time a
domain has finished scraping, including the pyrake stats collected. The email
will be sent to all recipients specified in the :setting:`STATSMAILER_RCPTS`
setting.

.. module:: pyrake.contrib.debug
   :synopsis: Extensions for debugging pyrake

Debugging extensions
--------------------

Stack trace dump extension
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. class:: pyrake.contrib.debug.StackTraceDump

Dumps information about the running process when a `SIGQUIT`_ or `SIGUSR2`_
signal is received. The information dumped is the following:

1. engine status (using ``pyrake.utils.engine.get_engine_status()``)
2. live references (see :ref:`topics-leaks-trackrefs`)
3. stack trace of all threads

After the stack trace and engine status is dumped, the pyrake process continues
running normally.

This extension only works on POSIX-compliant platforms (ie. not Windows),
because the `SIGQUIT`_ and `SIGUSR2`_ signals are not available on Windows.

There are at least two ways to send pyrake the `SIGQUIT`_ signal:

1. By pressing Ctrl-\ while a pyrake process is running (Linux only?)
2. By running this command (assuming ``<pid>`` is the process id of the pyrake
   process)::

    kill -QUIT <pid>

.. _SIGUSR2: http://en.wikipedia.org/wiki/SIGUSR1_and_SIGUSR2
.. _SIGQUIT: http://en.wikipedia.org/wiki/SIGQUIT

Debugger extension
~~~~~~~~~~~~~~~~~~

.. class:: pyrake.contrib.debug.Debugger

Invokes a `Python debugger`_ inside a running pyrake process when a `SIGUSR2`_
signal is received. After the debugger is exited, the pyrake process continues
running normally.

For more info see `Debugging in Python`.

This extension only works on POSIX-compliant platforms (ie. not Windows).

.. _Python debugger: http://docs.python.org/library/pdb.html
.. _Debugging in Python: http://www.ferg.org/papers/debugging_in_python.html
