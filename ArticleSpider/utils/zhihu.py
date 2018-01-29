# -*-encoding:utf-8-*-
import requests
import json
import time
import execjs


def main():

    class zhihu:

        phone = '+8618092671458'  # 手机号
        password = 'ty158917'  # 密码
        client_id = 'c3cef7c66a1843f8b3a9e6a1e3160e20'

        session = requests.Session()

        def __init__(self):

            if self.login():
                print('登录成功')
                self.getMyInfo()
            else:
                print('登录失败，出现验证码')

        def getSignature(self, timestamp):

            fp = open('./zhihu.js')
            js = fp.read()
            fp.close()
            ctx = execjs.compile(js)
            signature = ctx.call('getSignature', timestamp)
            return signature

        def login(self):

            headers = {
                'authorization': 'oauth ' + self.client_id,
                'Host': 'www.zhihu.com',
                'Origin': 'https://www.zhihu.com',
                'Referer': 'https://www.zhihu.com/signup?next=%2F',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/63.0.3239.84 Safari/537.36'
            }

            # 获取验证码票据(验证码cookie)
            captchaUrl = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'
            req = self.session.get(captchaUrl, headers=headers)
            print (req.text)
            captcha_info = json.loads(req.text)
            if captcha_info['show_captcha']:  # 出现验证码
                print('出现验证码')
                return False

            # 登录
            loginUrl = 'https://www.zhihu.com/api/v3/oauth/sign_in'
            timestamp = int(time.time() * 1000)
            signature = self.getSignature(timestamp)
            params = {
                'client_id': self.client_id,
                'grant_type': 'password',
                'timestamp': timestamp,
                'source': 'com.zhihu.web',
                'signature': signature,
                'username': self.phone,
                'password': self.password,
                'captcha': '',
                'lang': 'cn',
                'ref_source': 'homepage',
                'utm_source': ''
            }
            req = self.session.post(url=loginUrl, headers=headers, data=params)
            print(req.text)
            return True

        def getMyInfo(self):

            infoUrl = 'https://www.zhihu.com/api/v4/me?include=following_question_count'
            headers = {
                'Host': 'www.zhihu.com',
                'Referer': 'https://www.zhihu.com/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
            }
            req = self.session.get(url=infoUrl, headers=headers)
            json_data = json.loads(req.text)
            print(json_data)

    zhihu = zhihu()

if __name__ == '__main__':
    main()
