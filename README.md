# 2019.06.19 维护: FunpySpiderSearchEngine-ElasticSearch or Mysql 搜索引擎

>Scrapy1.6.0(爬取数据) + ElasticSearch6.8.0(存储数据并提供对外Restful Api) + Django 打造搜索引擎网站 (可配置数据存入Mysql)

[![Build Status](https://travis-ci.org/mtianyan/hexoBlog-Github.svg?branch=master)](https://travis-ci.org/mtianyan/hexoBlog-Github)
[![MIT Licence](https://badges.frapsoft.com/os/mit/mit.svg?v=103)](https://opensource.org/licenses/mit-license.php)

线上演示地址: 服务器到期暂无线上地址

>运行在旧笔记本版冒充服务器上使用frp内网穿透，不定时开启，如有强烈体验愿望, QQ: 1147727180

**本仓库为爬虫端数据入库ElasticSearch代码**,实现整个搜索需要结合Django网站端项目 https://github.com/mtianyan/mtianyanSearch

## 可用功能:

1. 伯乐在线，知乎爬虫存入Mysql & 存入ElasticSearch (拉勾暂不可用)
2. 全文搜索(需结合网站端一起使用)，搜索建议，我的搜索记录，搜索词高亮标红，搜索结果底部分页
3. Redis实现的实时三站已爬取数目展示，热门搜索Top-5

## 项目外部依赖

ElasticSearch6.8.0 + ElasticSearch-analysis-ik(中文分词) + Redis + Mysql

## 长期维护更新

定期对伯乐在线博客文章，拉勾网职位，知乎的问题回答爬取进行了维护更新，并进行了存入Mysql 以及 存入ElasticSearch6的测试。

## 如何开始使用？

安装ElasticSearch6.8.0,配置ElasticSearch-analysis-ik插件,安装Redis(可选配置ElasticSearch-head)

```
git clone https://github.com/mtianyan/FunpySpiderSearchEngine
# 新建数据库mtian_search; Navicat导入mysql文件; 修改config_template配置信息,去除_template后缀。
# 执行 sites/es_* 配置ELasticPipeline

cd FunpySpiderSearchEngine
pip install -r requirements.txt
scrapy crawl zhihu
scrapy crawl lagou
scrapy crawl jobbole
```

## TODO:

等待空闲，工作了太忙了

## 致谢 [原版视频课程地址:](https://coding.imooc.com/class/92.html)

>感谢Bobby老师的这门课程，通过这门课程学到了很多很多，自己在踩坑填坑，持续更新版本，时效更新，解决的时候，收获的不只有知识，我觉得更多是解决问题的能力。


## 关于我

一个学过php，做过安卓，摸过渗透，看过点前端，会写一点Python，最后发现自己啥也不会的肥宅在哭泣，欢迎加入有趣的Python群：619417153

**欢迎关注star项目！谢谢！你的关注支持是我继续分享前进的动力**

## 求打赏鼓励

很高兴我写的文章（或我的项目代码）对你有帮助，请我吃包辣条吧!

微信打赏:

![mark](http://myphoto.mtianyan.cn/blog/180302/i52eHgilfD.png?imageslim)

支付宝打赏:

![mark](http://myphoto.mtianyan.cn/blog/180302/gDlBGemI60.jpg?imageslim)
