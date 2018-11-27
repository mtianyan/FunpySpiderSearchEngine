from config import ZHIHU_PHONE, ZHIHU_PASSWORD

__author__ = 'mtianyan'
__date__ = '2018/8/21 07:19'
import time
from selenium import webdriver

browser = webdriver.PhantomJS()

browser.get("https://www.zhihu.com/")

browser.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[2]/span').click()
time.sleep(10)
browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(ZHIHU_PHONE)
browser.find_element_by_css_selector(".SignFlow-password input").send_keys(ZHIHU_PASSWORD)
browser.find_element_by_css_selector(".Button.SignFlow-submitButton").click()
