# -*- coding: utf-8 -*-
import re
from urllib import parse

import scrapy
from ArticleSpider.utils.common import OrderedSet
from ArticleSpider.items import FangItem


class FangSpider(scrapy.Spider):
    name = 'fang'
    allowed_domains = ['cd.fang.com']
    start_urls = ['http://newhouse.cd.fang.com/house/s/b91/']

    def parse(self, response):
        fang_list = response.css(".house_type.clearfix a::attr(href)").extract()
        fang_id_set = OrderedSet()
        for fang in fang_list:
            match_fang1 = re.match(".*list_900_(\d{10})_.*",fang)
            match_fang2 = re.match(".*/house/(\d{10})_.*",fang)
            fang_id = 0
            if match_fang1:
                fang_id = match_fang1.group(1)
                fang_id_set.add(fang_id)
            elif match_fang2:
                fang_id = match_fang2.group(1)
                fang_id_set.add(fang_id)
            else:
                continue
        fang_price_list = response.css(".nhouse_price span::text").extract()
        active_page_num = int(response.css(".fr a.active::text").extract_first())
        if active_page_num == 1:
            fang_name_list = response.css(".nlcd_name a::text").extract()[1:]
            fang_tag_list = response.css(".fangyuan").extract()[1:]
            fang_address_list = response.css(".address a::attr(title)").extract()[1:]
        else:
            fang_name_list = response.css(".nlcd_name a::text").extract()
            fang_tag_list = response.css(".fangyuan").extract()
            fang_address_list =response.css(".address a::attr(title)").extract()
            # 进行下一页下载
        for (fang_id, fang_name,fang_price,fang_address,fang_tag ) in zip(fang_id_set, fang_name_list,fang_price_list,fang_address_list,fang_tag_list):
            fang_item = FangItem()
            fang_item["id"] = fang_id
            fang_item["name"] = fang_name
            fang_item["price"] = fang_price
            fang_item["address"] = fang_address
            fang_item["tags"] = fang_tag
            yield fang_item
        next_url = "http://newhouse.cd.fang.com/house/s/b9{0}/".format(active_page_num+1)
        yield  scrapy.Request(parse.urljoin(response.url, next_url),callback=self.parse)
