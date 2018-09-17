---
title: Scrapy爬虫框架的使用（更新中）
date: 2018-09-17 20:31:54
tags: [python, 爬虫]
---
[Scrapy 官方文档](https://doc.scrapy.org/en/1.5/)
## 1. 创建自定义爬虫
    scrapy startproject zhihurb
<!--more-->

### 目录结构
    scrapy.cfg: 项目的配置文件(很少用)
    zhihurb/: 该项目的python模块。之后您将在此加入代码。
    zhihurb/items.py: 项目中的item文件.
    zhihurb/pipelines.py: 项目中的pipelines文件.
    zhihurb/settings.py: 项目的设置文件（设置）
    zhihurb/spiders/: 放置spider代码的目录.

### settings.py 常用配置
``` bash
LOG_LEVEL = 'ERROR'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
ROBOTSTXT_OBEY = False 
DOWNLOAD_DELAY = 1  下载延时
DEFAULT_REQUEST_HEADERS = {} 重新请求头
```

## 2. Scrapy框架中的xpath选择器
``` python
# 可以在命令行输入 scrapy shell [要测试的url地址]
response.xpath('//div[@class="tqtongji2"]/ul[position()>1]/li[1]/a/text()').extract() 进行测试

extract()  # Serialize and return the matched nodes as a list of unicode strings. Percent encoded content is unquoted. 

extract_first(default='not-found')  # return the first matched node.

re(regex) # Apply the given regex and return a list of unicode strings with the matches.
同样有re_first()

# 获取某节点所有文字内容
node = response.xpath('//div[@class="content"]')[0]
article = node.xpath('string(.)').extract_first()

```

## 3. 中断和恢复爬虫
    scrapy  crawl   article -s  JOBDIR=crawls/article
中断后，重新执行该命令，从暂停地方继续

## 4. 数据导出
    scrapy crawl heartsong  -o index.xml  
如果要简单将已抓取的item数据保存到文件，可以传递-o选项：格式包括 csv,json,xml

如果有复杂操作，在pipelines处理逻辑， 注释setting中的 ITEM_PIPELINES 配置项可以更换实现类。
```
ITEM_PIPELINES = {
   'music163.pipelines.MongoPipeline': 300,
}

```

###demo
``` python
from scrapy import Spider, Request
from zhihurb.items import ZhihurbItem
 
class ZhihuSpider(Spider):
    name = "zhihu"
    allowed_domains = ["zhihu.com"]
    start_urls = ['https://daily.zhihu.com/']

    def parse(self, response):
        urls = response.xpath('//div[@class="box"]/a/@href').extract()
        for url in urls:
            url = response.urljoin(url)
            print(url)
            yield Request(url, callback=self.parse_url)

    def parse_url(self, response):
        # name = xxxx
        # article = xxxx
        # 保存
        name = response.xpath('//h1[@class="headline-title"]/text()').extract_first()
        node = response.xpath('//div[@class="content"]')[0]
        article = node.xpath('string(.)').extract_first()
        item = ZhihurbItem()
        item['name'] = name
        item['article'] = article
     
        # 返回item
        yield item
```
## 补充: 爬取动态内容 使用selenium
``` python
path = 'https://mm.taobao.com/search_tstar_model.htm'
driver = webdriver.Chrome('/Applications/chromedriver')
# 获取图片url并下载
driver.get(path)
source = driver.page_source
tree = etree.HTML(source)
imgs = tree.xpath("//ul[@class='girls-list clearfix']/li/a/div/div[1]/img/@src")
names = [e.text for e in tree.xpath("//ul[@class='girls-list clearfix']/li/a/div/div[2]/span[1]")]
for i in names:
    print i

print '获取下一页'
driver.find_element_by_class_name("page-skip").send_keys('2')
driver.find_element_by_class_name("page-btn").click()
# 给浏览器足够时间打开下一页
time.sleep(1)
source = driver.page_source
tree = etree.HTML(source)
names = [e.text for e in tree.xpath("//ul[@class='girls-list clearfix']/li/a/div/div[2]/span[1]")]
for i in names:
    print i

# 最好还是js逆向工程，找到xhr请求
```


