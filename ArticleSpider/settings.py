# -*- coding: utf-8 -*-

# Scrapy settings for ArticleSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import os

BOT_NAME = 'ArticleSpider'

SPIDER_MODULES = ['ArticleSpider.spiders']
NEWSPIDER_MODULE = 'ArticleSpider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ArticleSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'ArticleSpider.middlewares.ArticlespiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'ArticleSpider.middlewares.ArticlespiderDownloaderMiddleware': 543,

    # 默认自带用户代理中间件需要none不使用
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    # 自定义的使用随机用户代理的中间件
    'ArticleSpider.middlewares.RandomUserAgentMiddlware': 400,
    # 为伯乐在线测试的Chrome集成。
    # 'ArticleSpider.middlewares.JSPageMiddleware': 1,

    # 随机更换西刺ip代理池中ip的中间件
    # 'ArticleSpider.middlewares.RandomProxyMiddleware': 2,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'ArticleSpider.pipelines.ArticlespiderPipeline': 300,

    # scrapy自带的三大法宝之一图片下载
    # 'scrapy.pipelines.images.ImagesPipeline': 1,

    # 我们自定义的图片下载pipeline:下载图片同时,保存路径
    'ArticleSpider.pipelines.ArticleImagePipeline': 2,

    # 自定义的保存数据到json文件中的pipeline。
    # 'ArticleSpider.pipelines.JsonWithEncodingPipeline': 3,

    # 调用scrapy提供的json export导出json文件
    # 'ArticleSpider.pipelines.JsonExporterPipeline': 4,

    # 使用同步方式写入数据库
    #  'ArticleSpider.pipelines.MysqlPipeline': 5,

    # 使用异步通用方式写入数据库
    'ArticleSpider.pipelines.MysqlTwistedPipeline': 6,

    # 将伯乐在线数据存入es中
    # 'ArticleSpider.pipelines.ElasticSearchPipeline': 7,
}

# 设置哪个字段是图片
IMAGES_URLS_FIELD = "front_image_url"
project_dir = os.path.abspath(os.path.dirname(__file__))
IMAGES_STORE = os.path.join(project_dir, 'images')


# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# mysql基本信息
MYSQL_HOST = "127.0.0.1"
MYSQL_DBNAME = "articlespider"
MYSQL_USER = "root"
MYSQL_PASSWORD = "tp158917"

# LOG_ENABLED = True
SQL_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
SQL_DATE_FORMAT = "%Y-%m-%d"

RANDOM_UA_TYPE = "random"

