import json
import os
import re
from datetime import datetime
from os import path
from urllib import parse
import scrapy
from scrapy.loader import ItemLoader

from FunpySpiderSearch.sites.zhihu.zhihu_item import ZhihuQuestionItem, ZhihuAnswerItem
from FunpySpiderSearch.utils.common import get_md5
from config import ZHIHU_PHONE, ZHIHU_PASSWORD


class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['https://www.zhihu.com/']

    # question的第一页answer的请求url
    start_answer_url = "https://www.zhihu.com/api/v4/questions/{0}/answers?include=data%5B%2A%5D.is_normal%2" \
                       "Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2" \
                       "Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2" \
                       "Cis_thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2" \
                       "A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit={1}&offset={2}&sort_by=default"

    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhizhu.com",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/68.0.3440.106 Safari/537.36"
    }

    custom_settings = {
        "COOKIES_ENABLED": True,
        "DOWNLOAD_DELAY": 1.5,
    }

    def parse(self, response):
        """
        提取出html页面中的所有url 并跟踪这些url进行一步爬取
        如果提取的url中格式为 /question/xxx 就下载之后直接进入解析函数
        """
        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        # 使用lambda函数对于每一个url进行过滤，如果是true放回列表，返回false去除。
        all_urls = filter(lambda x: True if x.startswith("https") else False, all_urls)
        for url in all_urls:
            # 具体问题以及具体答案的url我们都要提取出来，或关系
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)
            if match_obj:
                # 如果提取到question相关的页面则下载后交由提取函数进行提取
                request_url = match_obj.group(1)
                yield scrapy.Request(request_url, headers=self.headers, callback=self.parse_question)
            else:
                # 注释这里方便调试
                pass
                # 如果不是question页面则直接进一步跟踪
                yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def parse_question(self, response):
        # 处理question页面， 从页面中提取出具体的question item
        if "QuestionHeader-title" in response.text:
            # 处理新版本
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", response.url)
            if match_obj:
                question_id = int(match_obj.group(2))

            item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)

            item_loader.add_value("url_object_id", get_md5(response.url))
            item_loader.add_value("question_id", question_id)
            item_loader.add_css("title", "h1.QuestionHeader-title::text")
            item_loader.add_xpath("content", "//*[@id='root']/div/main/div/div[1]/div[2]"
                                             "/div[1]/div[1]/div[2]/div/div/div/span/text()")
            item_loader.add_css("topics", ".QuestionHeader-topics .Tag.QuestionTopic .Popover div::text")
            item_loader.add_css("answer_num", ".List-headerText span::text")
            item_loader.add_css("comments_num", ".QuestionHeader-Comment button::text")
            # 这里的watch_user_num 包含Watch 和 click 在clean data中分离
            item_loader.add_css("watch_user_num", ".NumberBoard-itemValue ::text")
            item_loader.add_value("url", response.url)
            question_item = item_loader.load_item()
        else:
            # 处理老版本页面的item提取(好像已经没有老版页面了我这里放着保险一下)
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", response.url)
            if match_obj:
                question_id = int(match_obj.group(2))

            item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
            item_loader.add_xpath("title",
                                  "//*[@id='zh-question-title']/h2/a/text()|//*[@id='zh-question-title']/h2/span/text()")
            item_loader.add_css("content", "#zh-question-detail")
            item_loader.add_value("url", response.url)
            item_loader.add_value("zhihu_id", question_id)
            item_loader.add_css("answer_num", "#zh-question-answer-num::text")
            item_loader.add_css("comments_num", "#zh-question-meta-wrap a[name='addcomment']::text")
            item_loader.add_xpath("watch_user_num", "//*[@id='zh-question-side-header-wrap']/text()|"
                                                    "//*[@class='zh-question-followers-sidebar']/div/a/strong/text()")
            item_loader.add_css("topics", ".zm-tag-editor-labels a::text")

            question_item = item_loader.load_item()
        # 发起向后台具体answer的接口请求
        yield scrapy.Request(self.start_answer_url.format(question_id, 20, 0), headers=self.headers,
                             callback=self.parse_answer)
        yield question_item

    def parse_answer(self, response):
        # 处理question的answer
        ans_json = json.loads(response.text)
        is_end = ans_json["paging"]["is_end"]
        next_url = ans_json["paging"]["next"]

        # 提取answer的具体字段
        for answer in ans_json["data"]:
            url_object_id = get_md5(url=answer["url"])
            answer_id = answer["id"]
            question_id = answer["question"]["id"]
            author_id = answer["author"]["id"] if "id" in answer["author"] else None
            author_name = answer["author"]["name"] if "name" in answer["author"] else None
            content = answer["excerpt"] if "excerpt" in answer else ""
            really_url = "https://www.zhihu.com/question/{0}/answer/{1}".format(answer["question"]["id"],
                                                                                answer["id"])
            create_time = answer["created_time"]
            updated_time = answer["updated_time"]

            yield scrapy.Request(really_url, headers=self.headers,
                                 callback=self.parse_answer_end, meta={'url_object_id': url_object_id,
                                                                       'answer_id': answer_id,
                                                                       'question_id': question_id,
                                                                       'author_id': author_id,
                                                                       'author_name': author_name,
                                                                       'content': content,
                                                                       'create_time': create_time,
                                                                       'updated_time': updated_time})
        if not is_end:
            yield scrapy.Request(next_url, headers=self.headers, callback=self.parse_answer)

    def parse_answer_end(self, response):
        answer_item = ZhihuAnswerItem()
        answer_item["url_object_id"] = response.meta.get("url_object_id", "")
        answer_item["answer_id"] = response.meta.get("answer_id", "")
        answer_item["question_id"] = response.meta.get("question_id", "")
        answer_item["author_id"] = response.meta.get("author_id", "")
        answer_item["author_name"] = response.meta.get("author_name", "")
        answer_item["content"] = response.meta.get("content", "")
        answer_item["url"] = response.meta.get("url", "")
        answer_item["create_time"] = response.meta.get("create_time", "")
        answer_item["update_time"] = response.meta.get("updated_time", "")
        answer_item["comments_num"] = response.css(".Button.VoteButton.VoteButton--up::text")[0].extract()
        answer_item["praise_num"] = response.css(".Button.ContentItem-action.Button--plain."
                                                 "Button--withIcon.Button--withLabel::text")[0].extract()
        answer_item["crawl_time"] = datetime.now()
        yield answer_item

    def start_requests(self):
        from selenium import webdriver
        import time
        browser = webdriver.PhantomJS()

        browser.get("https://www.zhihu.com/signin")
        browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(ZHIHU_PHONE)
        time.sleep(1)
        browser.find_element_by_css_selector(".SignFlow-password input").send_keys(ZHIHU_PASSWORD)
        time.sleep(2)
        browser.find_element_by_css_selector(".Button.SignFlow-submitButton").click()
        time.sleep(3)
        browser.get("https://www.zhihu.com/")
        time.sleep(6)
        zhihu_cookies = browser.get_cookies()
        print(zhihu_cookies)
        cookie_dict = {}
        import pickle
        for cookie in zhihu_cookies:
            base_path = path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cookies')
            f = open(base_path + "/zhihu/" + cookie['name'] + '.zhihu', 'wb')
            pickle.dump(cookie, f)
            f.close()
            cookie_dict[cookie['name']] = cookie['value']
        browser.close()
        return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict, headers=self.headers)]
