"""
This module contains the default values for all settings used by pyrake.

For more information about these settings you can read the settings
documentation in docs/topics/settings.rst

pyrake developers, if you add a setting here remember to:

* add it in alphabetical order
* group similar settings without leaving blank lines
* add its documentation to the available settings documentation
  (docs/topics/settings.rst)

"""

import os
import sys
from importlib import import_module
from os.path import join, abspath, dirname

AJAXCRAWL_ENABLED = False

BOT_NAME = 'pyrakebot'

CLOSESPIDER_TIMEOUT = 0
CLOSESPIDER_PAGECOUNT = 0
CLOSESPIDER_ITEMCOUNT = 0
CLOSESPIDER_ERRORCOUNT = 0

COMMANDS_MODULE = ''

COMPRESSION_ENABLED = True

CONCURRENT_ITEMS = 100

CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS_PER_IP = 0

COOKIES_ENABLED = True
COOKIES_DEBUG = False

DEFAULT_ITEM_CLASS = 'pyrake.item.Item'

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}

DEPTH_LIMIT = 0
DEPTH_STATS = True
DEPTH_PRIORITY = 0

DNSCACHE_ENABLED = True

DOWNLOAD_DELAY = 0

DOWNLOAD_HANDLERS = {}
DOWNLOAD_HANDLERS_BASE = {
    'file': 'pyrake.core.downloader.handlers.file.FileDownloadHandler',
    'http': 'pyrake.core.downloader.handlers.http.HTTPDownloadHandler',
    'https': 'pyrake.core.downloader.handlers.http.HTTPDownloadHandler',
    's3': 'pyrake.core.downloader.handlers.s3.S3DownloadHandler',
    'ftp': 'pyrake.core.downloader.handlers.ftp.FTPDownloadHandler',
}

DOWNLOAD_TIMEOUT = 180      # 3mins

DOWNLOADER = 'pyrake.core.downloader.Downloader'

DOWNLOADER_HTTPCLIENTFACTORY = 'pyrake.core.downloader.webclient.pyrakeHTTPClientFactory'
DOWNLOADER_CLIENTCONTEXTFACTORY = 'pyrake.core.downloader.contextfactory.pyrakeClientContextFactory'

DOWNLOADER_MIDDLEWARES = {}

DOWNLOADER_MIDDLEWARES_BASE = {
    # Engine side
    'pyrake.contrib.downloadermiddleware.robotstxt.RobotsTxtMiddleware': 100,
    'pyrake.contrib.downloadermiddleware.httpauth.HttpAuthMiddleware': 300,
    'pyrake.contrib.downloadermiddleware.downloadtimeout.DownloadTimeoutMiddleware': 350,
    'pyrake.contrib.downloadermiddleware.useragent.UserAgentMiddleware': 400,
    'pyrake.contrib.downloadermiddleware.retry.RetryMiddleware': 500,
    'pyrake.contrib.downloadermiddleware.defaultheaders.DefaultHeadersMiddleware': 550,
    'pyrake.contrib.downloadermiddleware.ajaxcrawl.AjaxCrawlMiddleware': 560,
    'pyrake.contrib.downloadermiddleware.redirect.MetaRefreshMiddleware': 580,
    'pyrake.contrib.downloadermiddleware.httpcompression.HttpCompressionMiddleware': 590,
    'pyrake.contrib.downloadermiddleware.redirect.RedirectMiddleware': 600,
    'pyrake.contrib.downloadermiddleware.cookies.CookiesMiddleware': 700,
    'pyrake.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 750,
    'pyrake.contrib.downloadermiddleware.chunked.ChunkedTransferMiddleware': 830,
    'pyrake.contrib.downloadermiddleware.stats.DownloaderStats': 850,
    'pyrake.contrib.downloadermiddleware.httpcache.HttpCacheMiddleware': 900,
    # Downloader side
}

DOWNLOADER_STATS = True

DUPEFILTER_CLASS = 'pyrake.dupefilter.RFPDupeFilter'

try:
    EDITOR = os.environ['EDITOR']
except KeyError:
    if sys.platform == 'win32':
        EDITOR = '%s -m idlelib.idle'
    else:
        EDITOR = 'vi'

EXTENSIONS = {}

EXTENSIONS_BASE = {
    'pyrake.contrib.corestats.CoreStats': 0,
    'pyrake.telnet.TelnetConsole': 0,
    'pyrake.contrib.memusage.MemoryUsage': 0,
    'pyrake.contrib.memdebug.MemoryDebugger': 0,
    'pyrake.contrib.closespider.CloseSpider': 0,
    'pyrake.contrib.feedexport.FeedExporter': 0,
    'pyrake.contrib.logstats.LogStats': 0,
    'pyrake.contrib.spiderstate.SpiderState': 0,
    'pyrake.contrib.throttle.AutoThrottle': 0,
}

FEED_URI = None
FEED_URI_PARAMS = None  # a function to extend uri arguments
FEED_FORMAT = 'jsonlines'
FEED_STORE_EMPTY = False
FEED_STORAGES = {}
FEED_STORAGES_BASE = {
    '': 'pyrake.contrib.feedexport.FileFeedStorage',
    'file': 'pyrake.contrib.feedexport.FileFeedStorage',
    'stdout': 'pyrake.contrib.feedexport.StdoutFeedStorage',
    's3': 'pyrake.contrib.feedexport.S3FeedStorage',
    'ftp': 'pyrake.contrib.feedexport.FTPFeedStorage',
}
FEED_EXPORTERS = {}
FEED_EXPORTERS_BASE = {
    'json': 'pyrake.contrib.exporter.JsonItemExporter',
    'jsonlines': 'pyrake.contrib.exporter.JsonLinesItemExporter',
    'jl': 'pyrake.contrib.exporter.JsonLinesItemExporter',
    'csv': 'pyrake.contrib.exporter.CsvItemExporter',
    'xml': 'pyrake.contrib.exporter.XmlItemExporter',
    'marshal': 'pyrake.contrib.exporter.MarshalItemExporter',
    'pickle': 'pyrake.contrib.exporter.PickleItemExporter',
}

HTTPCACHE_ENABLED = False
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_MISSING = False
HTTPCACHE_STORAGE = 'pyrake.contrib.httpcache.FilesystemCacheStorage'
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_IGNORE_SCHEMES = ['file']
HTTPCACHE_DBM_MODULE = 'anydbm'
HTTPCACHE_POLICY = 'pyrake.contrib.httpcache.DummyPolicy'

ITEM_PROCESSOR = 'pyrake.contrib.pipeline.ItemPipelineManager'

ITEM_PIPELINES = {}
ITEM_PIPELINES_BASE = {}

LOG_ENABLED = True
LOG_ENCODING = 'utf-8'
LOG_FORMATTER = 'pyrake.logformatter.LogFormatter'
LOG_STDOUT = False
LOG_LEVEL = 'DEBUG'
LOG_FILE = None

LOG_UNSERIALIZABLE_REQUESTS = False

LOGSTATS_INTERVAL = 60.0

MAIL_HOST = 'localhost'
MAIL_PORT = 25
MAIL_FROM = 'pyrake@localhost'
MAIL_PASS = None
MAIL_USER = None

MEMDEBUG_ENABLED = False        # enable memory debugging
MEMDEBUG_NOTIFY = []            # send memory debugging report by mail at engine shutdown

MEMUSAGE_ENABLED = False
MEMUSAGE_LIMIT_MB = 0
MEMUSAGE_NOTIFY_MAIL = []
MEMUSAGE_REPORT = False
MEMUSAGE_WARNING_MB = 0

METAREFRESH_ENABLED = True
METAREFRESH_MAXDELAY = 100

NEWSPIDER_MODULE = ''

RANDOMIZE_DOWNLOAD_DELAY = True

REDIRECT_ENABLED = True
REDIRECT_MAX_TIMES = 20  # uses Firefox default setting
REDIRECT_PRIORITY_ADJUST = +2

REFERER_ENABLED = True

RETRY_ENABLED = True
RETRY_TIMES = 2  # initial response + 2 retries = 3 requests
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 408]
RETRY_PRIORITY_ADJUST = -1

ROBOTSTXT_OBEY = False

SCHEDULER = 'pyrake.core.scheduler.Scheduler'
SCHEDULER_DISK_QUEUE = 'pyrake.squeue.PickleLifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'pyrake.squeue.LifoMemoryQueue'

SPIDER_MANAGER_CLASS = 'pyrake.spidermanager.SpiderManager'

SPIDER_MIDDLEWARES = {}

SPIDER_MIDDLEWARES_BASE = {
    # Engine side
    'pyrake.contrib.spidermiddleware.httperror.HttpErrorMiddleware': 50,
    'pyrake.contrib.spidermiddleware.offsite.OffsiteMiddleware': 500,
    'pyrake.contrib.spidermiddleware.referer.RefererMiddleware': 700,
    'pyrake.contrib.spidermiddleware.urllength.UrlLengthMiddleware': 800,
    'pyrake.contrib.spidermiddleware.depth.DepthMiddleware': 900,
    # Spider side
}

SPIDER_MODULES = []

STATS_CLASS = 'pyrake.statscol.MemoryStatsCollector'
STATS_DUMP = True

STATSMAILER_RCPTS = []

TEMPLATES_DIR = abspath(join(dirname(__file__), '..', 'templates'))

URLLENGTH_LIMIT = 2083

USER_AGENT = 'pyrake/%s (+http://pyrake.org)' % import_module('pyrake').__version__

TELNETCONSOLE_ENABLED = 1
TELNETCONSOLE_PORT = [6023, 6073]
TELNETCONSOLE_HOST = '127.0.0.1'

SPIDER_CONTRACTS = {}
SPIDER_CONTRACTS_BASE = {
    'pyrake.contracts.default.UrlContract': 1,
    'pyrake.contracts.default.ReturnsContract': 2,
    'pyrake.contracts.default.ScrapesContract': 3,
}
