# _*_ coding: utf-8 _*_
__author__ = 'mtianyan'
__date__ = '2017/6/24 17:17'

from selenium import webdriver
from scrapy.selector import Selector



#天猫价格获取
# browser.get("https://detail.tmall.com/item.htm?spm=a230r.1.14.3.yYBVG6&id=538286972599&cm_id=140105335569ed55e27b&abbucket=15&sku_properties=10004:709990523;5919063:6536025")
# t_selector = Selector(text=browser.page_source)
# print (t_selector.css(".tm-price::text").extract())
# # print (browser.page_source)
# browser.quit()

# #知乎模拟登陆
# browser.get("https://www.zhihu.com/#signin")
#
# browser.find_element_by_css_selector(".view-signin input[name='account']").send_keys("18487255487")
# browser.find_element_by_css_selector(".view-signin input[name='password']").send_keys("ty158917")
#
# browser.find_element_by_css_selector(".view-signin button.sign-button").click()


# #selenium 完成微博模拟登录
# browser.get("http://weibo.com/")
# import time
# time.sleep(5)
# browser.find_element_by_css_selector("#loginname").send_keys("1147727180@qq.com")
# browser.find_element_by_css_selector(".info_list.password input[node-type='password'] ").send_keys("tudoudou5283")
# browser.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()



# #开源中国博客
# browser.get("https://www.oschina.net/blog")
# import time
# time.sleep(5)
# for i in range(3):
#     browser.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
#     time.sleep(3)

# t_selector = Selector(text=browser.page_source)
# print (t_selector.css(".tm-promo-price .tm-price::text").extract())


# # 设置chromedriver不加载图片
# chrome_opt = webdriver.ChromeOptions()
# prefs = {"profile.managed_default_content_settings.images":2}
# chrome_opt.add_experimental_option("prefs", prefs)
#
# browser = webdriver.Chrome(executable_path="C:/chromedriver.exe",chrome_options=chrome_opt)
# browser.get("https://www.oschina.net/blog")


#phantomjs, 无界面的浏览器， 多进程情况下phantomjs性能会下降很严重

browser = webdriver.PhantomJS(executable_path="C:/phantomjs-2.1.1-windows/bin/phantomjs.exe")
browser.get("https://detail.tmall.com/item.htm?spm=a230r.1.14.3.yYBVG6&id=538286972599&cm_id=140105335569ed55e27b&abbucket=15&sku_properties=10004:709990523;5919063:6536025")
t_selector = Selector(text=browser.page_source)
print (t_selector.css(".tm-price::text").extract())
print (browser.page_source)
# browser.quit()