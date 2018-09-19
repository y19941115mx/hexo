---
title: pythonic 编程实践
date: 2018-09-13 20:22:22
tags: [编程, python]
---
> 众所周知 python作为解释性语言 它的执行速度和编译性语言相比 是非常慢的 它的优势在于  代码的易读和语法的简洁 为了发挥他的这些优势 写代码的时候 应该结合python的语法特性 写出真正pythonic的代码
<!--more-->

### 一行以蔽之
列表生成式是很强大的功能 适用于对列表或者字典进行的简单Map和Filter操作 
```python
# 处理list
l_result = [x.lower() for x in data if x.startswith('A') == 0]
# 处理dict
d_result = {k: v for k, v in mapdata.items() if v >= 30 and v < 100}
# 使用多层循环 注意嵌套的顺序
arr = [item for arr in two_d_arr for item in arr if item > 1] # two_d_arr = [[1, 2], [3, 4]]

```
行内表达式 包括元组自动解包和三元表达式，可以用来简化判断、交换 赋值操作 
```python
people = self.people or People() # 判空操作
result = 1 if xxx else 0  # 实现三元表达式
a, b = b, a # 行内交互元素
a, b = 1, 2 # 元祖自动解包，多个元素同时赋值
# 对应于列表s可以使用元祖解包取代列表索引和切片操作
#  day, mon, year = s 取代 s[0], s[1], s[2]分别赋值
# a,*rest,b = s 取代 s[0], s[1:-1], s[-1]分别赋值
```
### 使用生成器
生成器只保存算法，数据只在用到时再计算，配合for循环（迭代器）和列表生成式时能够大量节省内存
```python
# 在类中自定义生成器方法 生成固定长度的斐波那契数列
class fibClass(object):
    """docstring for fibClass"""
    def __init__(self, size):
        super(fibClass, self).__init__()
        self.size = size
    
    def get_fib(self):
        a, b, n = 0, 1, 0
        while n < self.size:
            yield a  # 一个函数定义中包含yield关键字 变为生成器函数
            a, b = b, a + b
            n = n + 1

if __name__ == '__main__':
    fib = fibClass(5)
    res = [i for i in fib.get_fib()]
    print(res)
```
### 函数装饰器
利用python高级函数的特性（可以将函数作为参数） 实现函数装饰器的功能 可以动态为函数填加功能
下面的例子给函数添加了计时功能，使用类的方式传值给装饰器 注意闭包的使用，在闭包的内函数中，我们可以随意使用外函数绑定来的变量，但是如果我们想修改外函数的变量数值的时候发现出问题了，在基本的python语法当中，一个函数可以随意读取全局数据，但是要修改全局数据的时候有两种方法:1 global 声明全局变量 2 全局变量是可变类型数据的时候可以修改。在闭包内函数也是类似的情况。在内函数中想修改闭包变量（外函数绑定给内函数的局部变量）的时候：
1. 在python3中，可以用nonlocal 关键字声明 一个变量，表示这个变量不是局部变量空间的变量，需要向上一层变量空间找这个变量。
2. 在python2中，没有nonlocal这个关键字，我们可以把闭包变量改成可变类型数据进行修改，比如列表或者字典.
```python
from time import  time, sleep
from datetime import datetime
class CallingInfo(object):
    def __init__(self, args= None):
        self.formatter = '%(func)s -> [%(time)s - %(used)s - %(ncalls)s]'
        # 传给装饰器的值
        self.args = args

    def info(self,func):
        # n = 0
        ncalls = {'n': 0}
        def wrapper(*args,**kwargs):
            now = datetime.now()
            start = time()
            # nonlocal  n
            # n += 1
            ncalls['n'] += 1
            res = func(*args,**kwargs)
            used = time() - start
            info = {}
            info['func'] = func.__name__
            info['time'] = now.strftime('%Y-%m-%d %H:%M:%S')
            info['used'] = used
            info['ncalls'] = ncalls['n']
            msg = self.formatter % info
            print(msg)
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
因为全局解释锁的存在，使用python多线程无法实现多cpu计算。通常用来处理多IO的操作，下面的例子使用一个线程处理文件 多个线程进行下载。使用线程安全的queue包中的Queue进行线程间通信。
```python
import requests, csv
from threading import Thread
from queue import Queue
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
            return re.text

    def run(self):
        print('Download',self.sid)
        data = self.download(self.url)
        self.queue.put((self.sid, data))

class ConvertThread(Thread):
    """docstring for ConvertThread"""
    def __init__(self,queue):
        super(ConvertThread, self).__init__()
        self.queue = queue
    
    def tocsv(self,data,fname):
        reader = csv.reader(data.split('x')) # 传入下载的csv文件的行分隔符 通常为'\n' 
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
# 启动多进程方式同多线程，这里采用函数式的方式 进程间无法访问主进程变量 不存在锁的问题
import multiprocessing

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

# 进程间通信
from multiprocessing import Queue
q = Queue()， # 父进程创建 并传给各个子进程
q.put() # 进程间通过Queue通信 方法同多进程
q.get()

```

### 常用内建模块
##### 字符串处理
**简单处理**
1. 分割字符串 str.split(',')默认为空格和\n、\t等特殊字符 或 使用字符串切片[m:n]
2. 去掉字符串中不需要的部分  str.strip('-+')  默认截取字符串前后的空格和特殊字符\n 可以传入特殊字符或使用str.replace(old, new)
3. 检查字符串的开头与结尾 str.startswith() str.endswith() 多个匹配传入元祖
4. 调整字符串中文本的格式 str.ljust(len, 填充字符) str.rjust() str.center()
5. 字符串拼接 '分割字符'.join(要拼接的字符串列表) 

**re 模块的使用**

初始化
 1.re.compile() 得到模式的对象pattern（re.compile(r'',re.I)忽视大小写）
再调用模块方法，例如 pattern.match(str) 
 2.re.match(pattern,str),直接使用模块方法，传入模式对象
re模块的常用方法
 1.split() 分割文本 返回分割字符串得到的列表 re.split(r':|,|、')可以用多个|连接多个分割符
 2.match(pattern,string) 只在字符串开头匹配字符串，返回第一个匹配的对象，如果不是开始位置匹配成功的话,就返回none
 3.search(pattern,string) 在整个字符串匹配字符，返回第一个匹配的对象 
 4.findall(pattern, string) 返回字符串中所有匹配正则表达式的子字符串
 5.sub(pattern,repl,string) 返回新的字符串,repl为替代值，可以为字符串、函数或组值
```python
# 使用函数 对替代值进行逻辑处理
def add1(match):
       val = match.group() # match 对象的group() 返回匹配到的字符串 groups()返回组值
       num = int(val) + 1
       return str(num)
# 正则中关于组的使用
re.sub(r'(\d{4})-(\d{2})-(\d{2})',r'\2:\3:\1',string) # 使用组用 \+相对位置 获取组值
re.sub(r'(?P<year>\d{4})-(?P<mon>\d{2})-(?P<day>\d{2})',r'\g<mon>/\g<day>/\g<year>', string) # 使用命名的方式获取组值

```

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

##### 更多内容
[廖大神的教程](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000)




