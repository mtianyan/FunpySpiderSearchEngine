# 2018.8.21重磅更新！！！: FunpySpiderSearch-ElasticSearch or Mysql 搜索引擎全面更新！！！

2018.08.21 最新可用Scrapy1.5.1爬取数据 + ElasticSearch6.3.2 存储数据并提供对外Restful Api + Django打造搜索引擎网站(可配置为存入Mysql)

[![Build Status](https://travis-ci.org/mtianyan/hexoBlog-Github.svg?branch=master)](https://travis-ci.org/mtianyan/hexoBlog-Github)
[![MIT Licence](https://badges.frapsoft.com/os/mit/mit.svg?v=103)](https://opensource.org/licenses/mit-license.php)

线上演示地址(近期重构更新中): http://search.mtianyan.cn

**本仓库为爬虫端数据入库ELasticSearch代码**

实现整个搜索需要结合mtianyanSearch项目(网站端) https://github.com/mtianyan/mtianyanSearch

## 可用功能:

1. 伯乐在线，拉勾职位，知乎爬虫存入Mysql 存入ELasticSearch
2. 全文搜索(需结合网站端一起使用)，搜索建议，我的搜索记录，搜索词高亮标红，底部分页
3. Redis实现的实时爬取数据展示(更新迭代中，演示站为历史数据，因此不会实时增长)，热门搜索Top-n

## 重磅更新一: 依赖全面更新，代码几乎完全重构

1. 将ElasticSearch的支持版本从rtf(5.1)版本解放，全面支持ElasticSearch最新版(6.3.2) + Elasticsearch-analysis-ik(中文分词)最新版,使用破坏性更新后的elasticsearch-dsl-py最新版本，不再需要为历史版本问题烦恼。
2. 项目代码完全重构,引入abc实现抽象类，抽象方法，规范并统一，Item接口设计

>items.py不再承担所有item编码，只规定对应想要完成目的实现的接口(设计了MySqlItem以及ElasticSearchItem)，具体的实体类型对象，均被整理至sites目录，以域名为归档标准

3. 将大多数的工具类，能抽取则抽取，并提供了很多辅助生成代码的help方法。(可查看utils下)
4. 使用了ELasticSearch6的全新接口，如Document(DocType的继任者，7.0时代的新主人), Index全新设计规范(从一库多表的类比官方限制为一库一表)，自定义analyzer实现对于Completion的自定义分析器设置
5. 统一命名规范: 域名+爬取内容+Item/Index，统一使用url_object_id 在Mysql中作为主键，ELasticSearch中作为meta.id，同时都进行了遇到重复，更新数据而不是新增，解决数据冗余。
6. 删除所有无用代码，保持项目简洁代码美观，所有代码进行了PEP8规范的格式整理

## 重磅更新二: 全面可用

在重构所有代码的同时对于伯乐在线博客文章，拉勾网职位，知乎的问题回答爬取进行了维护更新，并进行了存入Mysql与存入ELasticSearch6的通过性测试。

## 如何开始使用？

安装ELasticSearch6.3.2,配置Elasticsearch-analysis-ik插件,安装Redis(可选配置ELasticSearch-head)

```
git clone https://github.com/mtianyan/ArticleSpider
# 新建数据库mtiansearch  Navicat导入mysql文件;修改settings.py中数据库配置信息。
cd ArticleSpider
pip install -r req_funpySpider.txt
scrapy crawl zhihu
scrapy crawl lagou
scrapy crawl jobbole
```

#### 数据入库ELasticSearch配置。

执行site下的es_*文件，生成Mapping，setting中配置使用ELasticSearchPipeline

```
scrapy crawl zhihu
scrapy crawl lagou
scrapy crawl jobbole
```

## 致谢

[原版视频课程地址:](https://coding.imooc.com/class/92.html)

>感谢Bobby老师的这门课程，通过这门课程学到了很多很多，自己在踩坑填坑，重磅更新解决的时候，收获的不只有知识，我觉得更多是解决问题的能力。

简书相关文集地址(已过期，只有一定参考意义，最好的读物是源码！):

https://www.jianshu.com/nb/11202633

## 关于我

一个每天睡觉吃饭学政治数学英语学技术的今年刚毕业在家，不专心二战考研瞎折腾的家里蹲程序员(欢迎大家给我介绍很赚钱之道)

[简书](https://www.jianshu.com/u/db9a7a0daa1f) && [mtianyan's blog(暂时遗弃,懒)](http://blog.mtianyan.cn/)

有趣的Python群：619417153

**欢迎关注简书，star项目！谢谢！你的关注支持是我继续分享前进的动力**

## 求打赏鼓励

很高兴我写的文章（或我的项目代码）对你有帮助，请我吃包辣条吧!

微信打赏:

![mark](http://myphoto.mtianyan.cn/blog/180302/i52eHgilfD.png?imageslim)

支付宝打赏:

![mark](http://myphoto.mtianyan.cn/blog/180302/gDlBGemI60.jpg?imageslim)
