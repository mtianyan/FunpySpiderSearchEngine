>Word2vec 个性化搜索实现 +Scrapy2.3.0(爬取数据) + ElasticSearch7.9.1(存储数据并提供对外Restful API) + Django3.1.1 搜索

[![Build Status](https://travis-ci.org/mtianyan/hexoBlog-Github.svg?branch=master)](https://travis-ci.org/mtianyan/hexoBlog-Github)
[![MIT Licence](https://badges.frapsoft.com/os/mit/mit.svg?v=103)](https://opensource.org/licenses/mit-license.php)

**本仓库为爬虫端数据入库ElasticSearch代码**,实现整个搜索需要结合Django网站端项目 https://github.com/mtianyan/mtianyanSearch

## 可用功能:

1. 知乎答案问题爬虫存入ElasticSearch
2. 全文搜索(需结合网站端一起使用)，搜索词高亮标红
3. Redis实现的实时三站已爬取数目展示，热门搜索Top-5
4. word2vec改变ElasticSearch 评分， 比如历史上你搜索过Apple， 会使得Apple经过 Word2vec 计算出的苹果，乔布斯等关键词打分排名靠前

>word2vec 模型训练全过程请查看项目Word2VecModel 中README
>word2vec 使用，影响ElasticSearch打分，请查看mtianyanSearch中相关代码

## 项目演示图:

![](http://cdn.pic.mtianyan.cn/blog_img/20201004022048.png)

![](http://cdn.pic.mtianyan.cn/blog_img/20201004022236.png)

## 如何开始使用？

1. 安装ElasticSearch7.9.1, (可选配置ElasticSearch-head)
2. 配置ElasticSearch-analysis-ik插件
3. 安装Redis

### 本机运行

```
git clone https://github.com/mtianyan/FunpySpiderSearchEngine
# 修改config_template中配置信息后重命名为config.py
# 执行 sites/zhihu/es_zhihu.py

cd FunpySpiderSearchEngine
pip install -r requirements.txt
scrapy crawl zhihu
```

### Docker 运行

```
docker network create search-spider
git clone https://github.com/mtianyan/mtianyanSearch.git
cd mtianyanSearch
docker-compose up -d
git clone https://github.com/mtianyan/FunpySpiderSearchEngine
cd FunpySpiderSearchEngine
docker-compose up -d
```

访问127.0.0.1:8080

## 赞助

如果我的项目代码对你有帮助，请我吃包辣条吧!

![mark](http://myphoto.mtianyan.cn/blog/180302/i52eHgilfD.png?imageslim)