# encoding: utf-8
__author__ = 'mtianyan'
__date__ = '2018/1/23 0023 09:14'
import time
import re
from scrapy import Selector
from selenium import webdriver

browser = webdriver.Chrome(executable_path="./chromedriver.exe")


def parse_detail():
    id = 3210068104
    browser.get(
        "http://esf.cd.fang.com/newsecond/map/NewHouse/NewProjMap.aspx?newcode={0}".format(id))
    time.sleep(1)
    t_selector = Selector(text=browser.page_source)
    distance_lists = t_selector.xpath("//td/text()").extract()[1:]
    tag_names_list = t_selector.xpath("//th/text()").extract()
    for tag_name, distance in zip(tag_names_list, distance_lists):
        match_tag_name = re.match('【(.*)】(.*)', tag_name)
        if match_tag_name:
            tag = match_tag_name.group(1)
            nearname = match_tag_name.group(2)
        else:
            tag = ""
            nearname = ""
        match_distance = re.match('.*?(\d+)米', distance)
        if match_distance:
            distance = match_distance.group(1)
        else:
            distance = 0
        print(id, tag, nearname, distance)

if __name__ == "__main__":
    parse_detail()


# 上面是交通的。找猫画虎自己做后面。

browser.find_element_by_xpath('//*[@class="school"]').click()
time.sleep(1)
browser.find_element_by_xpath('//*[@class="hospital"]').click()