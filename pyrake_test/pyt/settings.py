BOT_NAME = 'pyt'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['pyt.spiders']
NEWSPIDER_MODULE = 'pyt.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

ITEM_PIPELINES = [
    'pyt.pipelines.MongoDBStorage',
]

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "pyt"
MONGODB_COLLECTION = "articles"