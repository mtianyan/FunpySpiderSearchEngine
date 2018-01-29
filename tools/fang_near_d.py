# encoding: utf-8
import csv
from selenium.webdriver.support.ui import WebDriverWait

__author__ = 'mtianyan'
__date__ = '2018/1/23 0023 09:14'
import time
import re
from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

browser = webdriver.Chrome(executable_path="./chromedriver.exe")
# browser = webdriver.Chrome()

info_transit = []
info_school = []
info_hospital = []
info_food = []
info_shopping = []
info_environment = []
id = 3211228186

wait = WebDriverWait(browser, 10)

browser.get(
    "http://esf.cd.fang.com/newsecond/map/NewHouse/NewProjMap.aspx?newcode={0}".format(id))
time.sleep(1)
t_selector = Selector(text=browser.page_source)


def get_transit_detail():
    distance_lists = t_selector.xpath("//td/text()").extract()[1:]
    tag_names_list = t_selector.xpath("//th/text()").extract()
    for tag_name, distance in zip(tag_names_list, distance_lists):
        match_tag_name = re.match('【(.*)】(.*)', tag_name)
        if match_tag_name:
            tag = match_tag_name.group(1).encode('gbk', 'ignore').decode('gbk')
            nearname = match_tag_name.group(2).encode('gbk', 'ignore').decode('gbk')
        else:
            tag = ""
            nearname = ""
        match_distance = re.match('.*?(\d+)米', distance)
        if match_distance:
            distance = match_distance.group(1).encode('gbk', 'ignore').decode('gbk')
        else:
            distance = 0
        info_school.append([id, tag, nearname, distance])
    get_school_button()


def get_school_button():
    school_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#btnSchool > span")))
    school_button.click()
    t_selector = Selector(text=browser.page_source)
    school_name_list = t_selector.xpath('//*[@id="divschool"]/table/tbody/tr/th/text()').extract()
    school_distance_list = t_selector.xpath('//*[@id="divschool"]/table/tbody/tr/td/text()').extract()
    for school_name, school_distance in zip(school_name_list, school_distance_list):
        school_tag_name = re.match('【(.*)】(.*)', school_name)
        if school_tag_name:
            school_tag = school_tag_name.group(1).encode('gbk', 'ignore').decode('gbk')
            school_name = school_tag_name.group(2).encode('gbk', 'ignore').decode('gbk')
        else:
            school_tag = ''
            school_name = ''
        match_distance = re.match('.*?(\d+)米', school_distance)
        if match_distance:
            school_distance = match_distance.group(1).encode('gbk', 'ignore').decode('gbk')
        else:
            school_distance = 0
        info_school.append([id, school_tag, school_name, school_distance])



        # def get_hospital_detail():
        #     browser.find_element_by_xpath('//*[@class="hospital"]').click()
        #     time.sleep(1)
        #     t_selector = Selector(text=browser.page_source)
        #     hospital_name_list = t_selector.xpath('//*[@id="divhospital"]/table/tbody/tr/th/text()').extract()
        #     hospital_distance_list = t_selector.xpath('//*[@id="divhospital"]/table/tbody/tr/td/text()').extract()
        #     for hospital_name, hospital_distance in zip(hospital_name_list, hospital_distance_list):
        #         match_tag_name = re.match('【(.*)】(.*)', hospital_name, re.S)
        #         if match_tag_name:
        #             hos_tag = match_tag_name.group(1).encode('gbk', 'ignore').decode('gbk')
        #             hos_name = match_tag_name.group(2).encode('gbk', 'ignore').decode('gbk')
        #         else:
        #             hos_tag = ""
        #             hos_name = ""
        #         match_distance = re.match('.*?(\d+)米', hospital_distance)
        #         if match_distance:
        #             hos_distance = match_distance.group(1).encode('gbk', 'ignore').decode('gbk')
        #         else:
        #             hos_distance = 0
        #         info_hospital.append([id, hos_tag, hos_name, hos_distance])
        # browser.close()
        # print(hos_tag, hos_name)


if __name__ == "__main__":
    get_transit_detail()
    print(info_school)

    # with open('Total.csv', 'w', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(['id', 'tag', 'nearname', 'distance', 'school_tag', 'school_name', 'school_distance'])
    #     for row in info_transit:
    #         writer.writerow(row)
    #     browser.close()
    # with open('School.csv', 'w', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(['id', 'school_tag', 'school_name', 'school_distance'])
    #     for row in info_school:
    #         writer.writerow(row)
    # with open('hospital.csv', 'w', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(['id', 'hos_tag', 'hos_name', 'hos_distance'])
    #     for row in info_hospital:
    #         writer.writerow(row)



    # 上面是交通的。找猫画虎自己做后面。

    # browser.find_element_by_xpath('//*[@class="school"]').click()
    # time.sleep(1)
    # browser.find_element_by_xpath('//*[@class="hospital"]').click()
