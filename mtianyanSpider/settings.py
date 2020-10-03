BOT_NAME = 'mtianyanSpider'

SPIDER_MODULES = ['mtianyanSpider.spiders']
NEWSPIDER_MODULE = 'mtianyanSpider.spiders'

ROBOTSTXT_OBEY = False

COOKIES_ENABLED = False

ITEM_PIPELINES = {
    'mtianyanSpider.pipelines.ElasticSearchPipeline': 400,
}

RANDOM_UA_TYPE = "random"
SQL_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
SQL_DATE_FORMAT = "%Y-%m-%d"
