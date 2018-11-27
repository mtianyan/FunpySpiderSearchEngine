import scrapy
from scrapy.http import Request
from urllib import parse

from FunpySpiderSearch.sites.jobbole.jobbole_Item import JobboleBlogItem, JobboleBlogItemLoader
from FunpySpiderSearch.utils.common import get_md5


class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = ['http://blog.jobbole.com/all-posts']

    def parse(self, response):
        """
        1. 获取文章列表页中的文章url交给scrapy下载并进行解析
        2. 获取下一页的url并交给scrapy进行下载,  下载完成后交给parse
        """
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            # 获取封面图的url
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            """
            post_url 是我们每一页的具体的文章url。
            下面这个Request是发起对文章详情页面的请求,使用回调函数每下载完一篇就callback进行这一篇的具体解析，将image_url进行了传递
            """
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url},
                          callback=self.parse_content)
        # 提取下一页url
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            # 如果还有next url 就调用下载下一页，回调parse函数找出下一页的url。
            # 调试时post_url 上线生产使用next_url
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    @staticmethod
    def parse_content(response):
        jobbole_item = JobboleBlogItem()
        # 通过item loader加载item
        front_image_url = response.meta.get("front_image_url", "")  # 文章封面图
        item_loader = JobboleBlogItemLoader(item=jobbole_item, response=response)

        # 通过css选择器将后面的指定规则进行解析。
        item_loader.add_css("title", ".entry-header h1::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        item_loader.add_value("front_image_url", [front_image_url])
        item_loader.add_css("praise_nums", ".vote-post-up h10::text")
        item_loader.add_css("comment_nums", "a[href='#article-comment'] span::text")
        item_loader.add_css("fav_nums", ".bookmark-btn::text")
        item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
        item_loader.add_css("content", "div.entry")

        # 调用这个方法来对规则进行解析生成item对象
        jobbole_item = item_loader.load_item()

        # 已经填充好了值调用yield传输至pipeline
        yield jobbole_item
