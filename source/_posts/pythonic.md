---
title: pythonic 编程实践
date: 2018-09-13 20:22:22
tags: [编程, python]
---
> 众所周知 python作为解释性语言 它的执行速度和编译性语言相比 是非常慢的 它的优势在于  代码的易读和语法的简洁 为了发挥他的这些优势 写代码的时候 应该结合python的语法特性 写出真正pythonic的代码
> <!--more-->

### 一行以蔽之
列表生成式是很强大的功能 适用于对列表或者字典进行的简单Map和Filter操作
```python
# 使用列表解析
l_result = [x.lower() for x in data if x.startswith('A') == 0]

d_result = {k: v for k, v in mapdata.items() if v >= 30}

```
行内表达式 可以用来简化判断、交换 赋值操作
```python
people = self.people or People() # 判空操作
result = 1 if xxx else 0  # 实现三元表达式
a, b = b, a # 行内交互元素
a, b = 1, 2 # 行内多个元素赋值
```
### 使用生成器
生成器是python中的特有功能 结合python中的for循环 能够写出更加灵活的代码 下面的例子是使用生成器 实现可迭代对象 实现循环时访问网络
```python

class weatherIterable:
    def __init__(self, cities):
        self.cities = cities

    def getweather(self, city):
        r = requests.get("http://wthrcdn.etouch.cn/weather_mini?city=" + city)
        data = r.json()['data']['forecast'][0]
        return "%s:%s , %s" % (city, data['low'],data['high'])
    
    def __iter__(self):
        for city in self.cities:
            yield self.getweather(city)

x = weatherIterable(['天津', '合肥'])

for i in x:
    print(i)
```
### 函数装饰器
利用python高级函数的特性（可以将函数作为参数） 实现函数装饰器的功能 可以动态为函数填加功能

---

下面的例子给函数添加了计时功能，使用类的方式传值给装饰器 注意闭包的使用 如果传递的闭包变量在 返回的函数中发生改变 则 要使用可变对象（例如list或dict）
```python
import logging
from time import  time, sleep
from datetime import datetime
class CallingInfo(object):
    def __init__(self, name):
        log = logging.getLogger(name)
        log.setLevel(logging.INFO)
        fh = logging.FileHandler(name+'.log')
        log.addHandler(fh)
        log.info('Start'.center(50,'-'))
        self.log = log
        self.formatter = '%(func)s -> [%(time)s - %(used)s - %(ncalls)s]'
    
    def info(self,func):
        ncalls = {'n': 0}
        def wrapper(*args,**kwargs):
            now = datetime.now()
            start = time()
            ncalls['n'] += 1
            res = func(*args,**kwargs)
            used = time() - start
            info = {}
            info['func'] = func.__name__
            info['time'] = now.strftime('%Y-%m-%d %H:%M:%S')
            info['used'] = used
            info['ncalls'] = ncalls['n']
            msg = self.formatter % info
            self.log.info(msg)
            return res
        return wrapper

cinfo =CallingInfo('mylog')

@cinfo.info
def f():
    print('in f')

for _ in range(10):
    f()

```

### 类的设计
类似java为类中属性定义的set、get方法 python 提供了@property装饰器 下面的例子中：birth是可读写属性，而age就是一个只读属性 直接赋值 编译器会报错。
```python
class Student(object):
    @property
    def birth(self):
        return self._birth

    @birth.setter
    def birth(self, value):
        self._birth = value

    @property
    def age(self):
        return 2015 - self._birth

```
python中有很多以__XXX___ 命名的魔术方法 使用它们能够帮助我们更好的定制类

#### 常用的魔术方法
方法名 | 说明
---|---
\_\_bool__(self)     | 定义对象被作为bool值时的行为，返回 True 或 False 
\_\_call__(self) | 定义对象被作为函数调用时的行为
\_\_getitem__(self) | 定义获取对象中指定元素的行为，相当于 self[key]
\_\_setitem__(self) | 定义设置对象中指定元素的行为，相当于 self[key] = value
\_\_iter__(self) | 定义当迭代对象时的行为

#### 让对象支持比较操作
用total_ordering装饰类后,不需要重写所有的 比较方法 只需要重写两个比较方法
```python
from functools import total_ordering
@total_ordering
class Circle:
    def __init__(self,r):
        self.r = r 
        self.s = 3.14 * r ** 2
    def __eq__(self,obj):
        return self.s == obj.s
    def __lt__(self,obj):
        return self.s < obj.s
```

### 多进程和多线程
使用多线程实现多io 单cpu计算的任务。使用stringIO和bytesIO代替临时文件
```python
import requests, csv
from threading import Thread
from queue import Queue
from io import BytesIO
class DownloadThread(Thread):
    """docstring for DownloadThread"""
    def __init__(self, sid, queue):
        super(DownloadThread, self).__init__()
        self.sid = sid 
        self.url = "http://table.finance.yahoo.com/table.csv?s=%s.sz"
        self.url %= str(sid).rjust(6,'0')
        self.queue = queue
    
    def download(self, url):
        re = requests.get(self.url,timeout=3)
        if re.status_code == 200:
            return BytesIO(re.content)

    def run(self):
        print('Download',self.sid)
        data = self.download(self.url)
        self.queue.put((self.sid, data))

class ConvertThread(Thread):
    """docstring for ConvertThread"""
    def __init__(self,queue):
        super(ConvertThread, self).__init__()
        self.queue = queue
    
    def tocsv(self,rf,fname):
        reader = csv.reader(rf)
        with open(fname,'w') as wf:
            writer = csv.writer(wf)
            writer.writerow(next(reader))
            for line in reader:
                '''找2016年1月1日后且交易额大于5千万的写入pingan2.csv'''
                if line[0] < '2016-01-01':
                    break
                if int(line[5]) > 50000000:
                    writer.writerow(line)
    
    def run(self):
        while True:
            sid, data = self.queue.get()
            print('convert',sid)
            if sid == -1:
                break
            if data:
                fname = 'result_%s.csv' % str(sid)
                self.tocsv(data,fname)

if __name__ == '__main__':
    q = Queue()
    dThreads = [DownloadThread(i, q) for i in range(1,5)]
    cThread = ConvertThread(q)
    for t in dThreads:
        t.start()
    cThread.start()
    for t in dThreads:
        t.join()
    q.put((-1, None))

```
使用多进程 计算多个cpu密集型任务
```python
# 启动多进程方式同多线程，但是进程间无法访问本地变量 不存在锁的问题
from multiprocessing import Process

def process_link_crawler():
    num_cpus = multiprocessing.cpu_count()
    print('num_cpus:', num_cpus)
    process = []
    for i in range(num_cpus):
        p = multiprocessing.Process(target=main)
        p.start()
        process.append(p)
    for p in process:
        p.join()

# 如果要启动大量的子进程，可以用进程池的方式批量创建子进程：
from multiprocessing import Pool
p = Pool(3)
p.apply_async(long_time_task, args=(i,))

# 进程间通信：Python的multiprocessing模块包装了底层的机制，提供了Queue、Pipe等多种方式来交换数据
from multiprocessing import Queue
q = Queue()， # 父进程创建 并传给各个子进程
q.put() # 进程间通过Queue通信 方法同多进程
q.get()

```

### 常用内建模块
##### 字符串处理
###### 简单处理
1. 分割字符串 str.split() 或 字符串切片
2. 去掉字符串中不需要的部分  str.strip('-+')  默认截取字符串前后的空格和特殊字符\n 可以传入特殊字符 
或str.replace()
3. 检查字符串的开头与结尾 str.startswith() str.endswith() 多个匹配传入元祖
4. 调整字符串中文本的格式 str.ljust(len, 填充字符) str.rjust() str.center()
5. 字符串拼接 '分割字符'.join(要拼接的字符串列表) 

###### re 模块的两种使用方式

1. 首先 生成模式对象。再调用模块的方法
  - re.compile() 得到模式的对象pattern（re.compile(r'',re.I)忽视大小写）
  - pattern.match(str) 再调用match方法，match对象有group(),span()，groups()对分组操作
2. 类似re.match(pattern,str),直接使用模块方法，传入其他相同。

re模块的方法
找到一个匹配项：
1. match(pattern,string) 只在字符串开头匹配字符串，返回match对象，如果不是开始位置匹配成功的话，match()就返回none,
2. search(pattern,string) 在整个字符串匹配字符,方法同match
查找所有匹配：
3. findall(pattern, string) 返回正则匹配部分组成的列表
4. sub(pattern,repl,string) 返回新的字符串,repl为替代值，可以为字符串或函数:
```
def add1(match):
       val = match.group()
       num = int(val) + 1
       return str(num)
```
re.sub(r'(\d{4})-(\d)-(\d)',r'\2:\3:\1',string) 使用组用 \+相对位置 获取组值

re.sub(r'(?P<year>\d{4})-(P<day>\d)',r'\g<mon>/\g<day>/\g<year>', s)
分割文本：
5. re.split() 返回分割字符串得到的列表
re.split(r':|,|、')可以用多个|连接多个分割符


##### 文件与目录处理
操作文件和目录的函数一部分放在os模块中，一部分放在os.path模块中

API | 操作
---|---
os.path.abspath('.') | 查看当前目录的绝对路径
os.listdir('.') | 查看当前目录下的所有文件和文件夹
os.path.isdir(x) | 判断是否为目录
os.mkdir('/Users/michael/testdir') | 创建一个目录
os.rmdir('/Users/michael/testdir') | 删除一个目录
os.path.join('fdir', 'sdir')/os.path.split() | 在某个目录下创建一个新目录
os.path.splitext() | 可以直接得到文件扩展名，很多时候非常方便
os.rename('test.txt', 'test2.py')| 修改文件名
os.remove('test.py') | 删掉文件
os.isfile(x)| 判断x是否为文件
```bash
# 查看当前目录的绝对路径:
>>> 
'/Users/michael'
# 在某个目录下创建一个新目录，首先把新目录的完整路径表示出来:
>>> os.path.join('/Users/michael', 'testdir')
'/Users/michael/testdir'
# 然后创建一个目录:
>>> os.mkdir('/Users/michael/testdir')
# 删掉一个目录:
>>> os.rmdir('/Users/michael/testdir')
# 获取文件扩展名
>>> os.path.splitext('/path/to/file.txt')
('/path/to/file', '.txt')
# 列出当前目录下所有的.py文件
>>> [x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1]=='.py']
['apis.py', 'config.py', 'models.py', 'pymonitor.py', 'test_db.py', 'urls.py', 'wsgiapp.py']
```


##### 日期与时间处理
```bash
>>> from datetime import datetime
>>> now = datetime.now() # 获取当前datetime
>>> print(now)
2015-05-18 16:28:07.198690

>>> from datetime import datetime
>>> dt = datetime(2015, 4, 19, 12, 20) # 用指定日期时间创建datetime
>>> print(dt)
2015-04-19 12:20:00

>>> from time import time, sleep
>>> time() # 获取当前秒数 常用来计时
1536841053.011322 
>>> sleep() # 程序睡眠
```
![转换关系.jpg](https://ws2.sinaimg.cn/large/0069RVTdgy1fv86si9gs0j30qi01xq3g.jpg)
这里没有考虑到时区 如果涉及到多个时区的转换处理
[查看更多详细内容](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001431937554888869fb52b812243dda6103214cd61d0c2000)

##### 图像处理
```python
from PIL import Image
# 图片缩放
# 打开一个jpg图像文件，注意是当前路径:
im = Image.open('test.jpg')
# 获得图像尺寸:
w, h = im.size
print('Original image size: %sx%s' % (w, h))
# 缩放到50%:
im.thumbnail((w//2, h//2))
print('Resize image to: %sx%s' % (w//2, h//2))
# 把缩放后的图像用jpeg格式保存:
im.save('thumbnail.jpg', 'jpeg')

# 图片模糊
# 打开一个jpg图像文件，注意是当前路径:
im = Image.open('test.jpg')
# 应用模糊滤镜:
im2 = im.filter(ImageFilter.BLUR)
im2.save('blur.jpg', 'jpeg')

```




