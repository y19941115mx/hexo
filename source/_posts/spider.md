---
title: 爬虫技术基础
date: 2018-09-17 20:20:12
tags: [python, 爬虫]
---
>这里主要介绍了两个爬虫中最常使用的库，requests和xpath。
### 安装requests
```python
    pip install requests
```
<!--more-->
### 发送请求
* Get 查看资源
* POST 增加资源
* PUT 修改资源     
* PATCH 少量修改资源
* DELETE 删除资源
* HEAD 查看响应头
* OPTIONS 查看可用的请求方法

#### api
* get 方式 后面跟拼接参数:   requests.get(url, params={'key1':'value1'})
* 表单参数提交: requests.post(url, data={'key1':'value1','key2':'value2'})
* json 参数提交  requests.post(url, json={'key1':'value1','key2':'value2'})
* 提交文件 requests.post(url, files={'file':open('sss.csv','rb')})

#### 异常处理（异常放在requests.exceptions包内）
1. 请求超时处理：except exceptions.Timeout
requests.get(url, timeout=10)
2. 错误码异常处理 except exceptions.HTTPError
如果响应的状态码不为200，response.raise_for_status() 会抛出状态码异常：response.raise_for_status()
``` python
import requests
from requests.exceptions import Timeout, ConnectionError, RequestException,.HTTPError
 
try:
    resp = requests.get('http://httpbin.org/get', timeout=0.5)
    print(resp.status_code)
except Timeout: # 访问超时的错误
    print('Timeout')
except ConnectionError: # 网络中断连接错误
    print('Connect error')
except RequestException: # 父类错误
    print('Error')
except HTTPError: # 错误码
    print('响应状态非200')

```

#### Demo
```python
//伪造头信息
headers = {"Host":" music.163.com",

"User-Agent":" Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0",

}
requests.get(url,headers = headers)

#  文件上传
files = {'file' : open('logo.gif','rb')}
resp = requests.post('http://httpbin.org/post', files=files)
```

### 解析响应
#### 响应状态码：
``` bash
1XX:消息

2XX 请求成功：
200 返回响应成功 201 资源建立成功 204 成功响应，无返回  

3XX 重定向：
301 永久移动 302 暂时移动 304 上次的get请求访问过的内容

4XX 客户端错误：
400 请求有问题 401 认证问题 403 权限不足，服务器拒绝执行 404 页面不存在

5XX 服务器端错误：
500 服务器端有bug 501 无法识别请求的方法502 网关错误 503 服务不可用
```
#### api        
* status_code 状态码

* reason 响应情况 

* headers 获取响应头

* url(  响应的地址

* request 获得响应对应的请求的对象，有headers 和 body

* content() 读取二进制内容 常用于图片下载

* text() 解析为解码后的字符串(可以修改requests.encoding = 'utf-8' 默认是utf-8)

* json() 将json格式的响应解析为python中的字典

### requests demo
``` python
一.图片下载
from contextlib import closing
url = 'http://pic.58pic.com/58pic/16/42/96/56e58PICAu9_1024.jpg'
 #伪造头信息
 headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) 
Gecko/20100101 Firefox/51.0'}
#关闭流的方式发送请求
 with closing(requests.get(url,headers=headers)) as response:
 with open('demo.jpg','wb') as f:
#每128个字节写入一次文件
        for chunk in response.iter_content(128):
            f.write(chunk)
```
### requests使用进阶
1.基本认证，验证账号与密码requests.get(url,auth=(name,password))
2.OAUTH认证
``` python
from requests.auth import AuthBase

class GitHubAuth(AuthBase):
def __init__(self, token):
  self.token= token
def __call__(self,r):
#request 加headers
  r.headers['Authorization'] = '  '.join(['token', self.token])
def oauth_advanced():
  #传入access token
auth = GithubAuth('dddsfsdfsdfasf')
response = requests.get(url,auth = auth)
```
3.代理设置 有些网站会限制 IP 访问频率，超过频率就断开连接。这个时候我们就需要使用到代理，我们可以通过为任意请求方式提供`proxies`参数来配置单个请求。

``` python
import requests
 
proxies = {
    "http": "http://10.10.1.10:3128",
    "https": "http://10.10.1.10:1080",
}
resp = requests.get('http://www.baidu.com', proxies=proxies)
print(resp.status_code)
```

也可以通过环境变量 `HTTP_PROXY` 和 `HTTPS_PROXY` 来配置代理。
有些代理需要加上用户名和密码的，代理可以使用`http://user:password@host/`语法，比如：

``` python
proxies = {
    "http": "http://user:pass@10.10.1.10:3128/",
}
```

### xpath安装
    pip install lxml
### xpathDemo
``` python
from lxml import etree
# 字符串读取html
html_str = '''  
<div>
    <ul>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
     </ul>
 </div>


html = etree.HTML(html_str)
#也可以从文件读取html html = etree.parse('hello.html') 

res = html.xpath("//div/ul/li[@class='item-0']/a")

for e in res:
    print(e.text)
    print(e.get("href"))
```

### xpath语法
```
1. 获取 <li> 标签的所有 class
result = html.xpath('//li/@class')
print result
运行结果:
['item-0', 'item-1', 'item-inactive', 'item-1', 'item-0']

2. 获取 <li> 标签下 href 为 link1.html 的 <a> 标签
result = html.xpath('//li/a[@href="link1.html"]')
print result
运行结果
[<Element a at 0x10ffaae18>]

3. 获取 <li> 标签下的所有 <span> 标签
不能这样写：result = html.xpath('//li/span')
因为 / 是用来获取子元素的，而 <span> 并不是 <li> 的子元素，所以，要用双斜杠

result = html.xpath('//li//span')
print result
运行结果
[<Element span at 0x10d698e18>]

4. 获取 <li> 标签下的所有 class，不包括 <li>
result = html.xpath('//li/a//@class')
print result
运行结果
['blod']

5. 获取最后一个 <li> 的 <a> 的 href
result = html.xpath('//li[last()]/a/@href')
print result
运行结果
['link5.html']

6. 获取倒数第二个元素的内容
result = html.xpath('//li[last()-1]/a')
print result[0].text
运行结果
fourth item

7. 获取 class 为 bold 的标签名
result = html.xpath('//*[@class="bold"]')
print result[0].tag
运行结果
span

```
### xpath进阶用法
``` python
# 对节点进行xpath查询 处理字段缺失
tables = html.xpath("//div[@class='indent']//table")
for table in tables:
            score = table.xpath("//span[@class='rating_nums']")[0].text
            description = "暂无简介"
            node = table.xpath("//span[@class='inq']")
            if node:
                description = node[0].text

# 获取某节点内所有文字内容
# <li class="item-1">sss <a href="link2.html">second item</a> ss</li>
res = html.xpath('//li')[0]

text = res.xpath('string(.)')
print(l1)

# 结果： sss second item ss
```
### 爬虫进阶
MongoDB的使用 设置下载缓存和实现多进程爬取
[demo](https://github.com/y19941115mx/CrawlingLyric)

### 相关教程
[爬虫教程](http://www.jqhtml.com/13259.html)

