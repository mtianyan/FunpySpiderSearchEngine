# encoding: utf-8
import re

__author__ = 'mtianyan'
__date__ = '2018/1/22 0022 19:42'

import requests
from scrapy.selector import Selector
import MySQLdb

conn = MySQLdb.connect(
    host="127.0.0.1",
    user="root",
    passwd="tp158917",
    db="articlespider",
    charset="utf8")
cursor = conn.cursor()


def crawl_ips():
    # 爬取西刺的免费ip代理
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}
    for i in range(1568):
        res = requests.get(
            "http://www.xicidaili.com/nn/{0}".format(i),
            headers=headers)

        selector = Selector(text=res.text)
        all_trs = selector.css("#ip_list tr")

        ip_list = []
        for tr in all_trs[1:]:
            speed_str = tr.css(".bar::attr(title)").extract()[0]
            if speed_str:
                speed = float(speed_str.split("秒")[0])
            all_texts = tr.css("td::text").extract()
            match_obj1 = re.match(".*'HTTPS'.*", str(all_texts))
            match_obj2 = re.match(".*'HTTP'.*", str(all_texts))
            proxy_type = ""
            if match_obj1:
                proxy_type = "HTTPS"
            elif match_obj2:
                proxy_type = "HTTP"
            ip = all_texts[0]
            port = all_texts[1]

            ip_list.append((ip, port, proxy_type, speed))

        for ip_info in ip_list:
            cursor.execute(
                "insert proxy_ip(ip, port, speed, proxy_type) VALUES('{0}', '{1}', {2}, '{3}')".format(
                    ip_info[0], ip_info[1], ip_info[3], ip_info[2]))

            conn.commit()


class GetIP(object):
    def delete_ip(self, ip):
        # 从数据库中删除无效的ip
        delete_sql = """
            delete from proxy_ip where ip='{0}'
        """.format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def judge_ip(self, ip, port):
        # 判断ip是否可用
        http_url = "https://www.baidu.com"
        proxy_url = "http://{0}:{1}".format( ip,port)
        try:
            proxy_dict = {
                "http": proxy_url,
            }
            response = requests.get(http_url, proxies=proxy_dict)
        except Exception as e:
            print(ip)
            print ("invalid ip and port")
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 300:
                print ("valid ip")
                return True
            else:
                print ("invalid ip and port")
                self.delete_ip(ip)
                return False

    def get_random_ip(self):
        # 从数据库中随机获取一个可用的ip
        random_sql = """
              SELECT ip, port FROM proxy_ip WHERE proxy_type ='HTTP'
            ORDER BY RAND()
            LIMIT 1
            """
        result = cursor.execute(random_sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]


            judge_re = self.judge_ip(ip, port)
            if judge_re:
                return "http://{0}:{1}".format(ip, port)
            else:
                return self.get_random_ip()


# print (crawl_ips())
if __name__ == "__main__":
    get_ip = GetIP()
    get_ip.get_random_ip()
