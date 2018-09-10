import qiniu
import urllib
import sys
import os
import datetime

__author__ = "victro"


"""
将图片拖曳到此脚本即可自动上传到七牛云
"""

# ----------------手动配置区---------------
accessKey = 'kmts9lL8CCE6qmjYFJoDgTTBwnSf8HpT0josPWFV'
secretkey = 'fttkg-9VrJ-JZhrNJAqFww6_qL_SyNgW5QsIsGBI'
# 上传空间的域名，需要自己去后台获取
bucket_url = {
    'victor': 'pel4qfee1.bkt.clouddn.com/',
}
bucket = 'victor'  # 上传空间

# ----------------默认配置区-------------------------
img_suffix = ["jpg", "jpeg", "png", "bmp", "gif"]


class Qiniu(object):

    """七牛上传与下载的工具类

    需要七牛的Python SDK
    pip install qiniu
    SDK详细用法见　http://developer.qiniu.com/docs/v6/sdk/python-sdk.html
    """
    SUCCESS_INFO = "上传成功！"

    def __init__(self, accessKey, secretkey):
        self.accessKey = accessKey
        self.secretkey = secretkey
        self._q = qiniu.Auth(self.accessKey, self.secretkey)

    def upload_file(self, bucket, up_filename, file_path):
        """上传文件

        Args:
            bucket: 上传空间的名字
            up_filename: 上传后的文件名
            file_path:   本地文件的路径
        Returns:
            ret:     dict变量，保存了hash与key（上传后的文件名）
            info:    ResponseInfo对象，保存了上传信息
            url:     st, 上传后的网址
        """
        token = self._q.upload_token(bucket)
        ret, info = qiniu.put_file(token, up_filename, file_path)
        url = self.get_file_url(bucket, up_filename)
        return ret, info, url

    def get_file_url(self, bucket, up_filename):
        if not bucket in bucket_url.keys():
            raise AttributeError("空间名不正确！")
        url_prefix = bucket_url[bucket]
        url = url_prefix + urllib.parse.quote(up_filename)
        return url


def transform(filename, url):
    result_str = ''
    line = "[%s](%s)\n" % (filename, url)
    # 如果是图片则生成图片的markdown格式引用
    if os.path.splitext(filename)[1][1:] in img_suffix:
        line = "!" + line
    result_str += line + '\n'
    return result_str


def getTimeStr():
    """返回 2015/11/18/17/16/8/ 形式的字符串

    如果上传同名文件且前缀相同，则后上传的文件会顶掉先前的
    加时间作为前缀，即便于检索，又避免此问题
    """
    now = datetime.datetime.now()
    tmp = tuple(now.timetuple())[:-3]
    tmp = map(str, tmp)
    return "/".join(tmp) + "/"

if __name__ == '__main__':
    res = '上传结果: \n'
    if len(sys.argv) == 1:
        print("请将文件拖曳到本脚本！")
        sys.exit(0)
    files = sys.argv[1:]

    q = Qiniu(accessKey, secretkey)
    timeStr = getTimeStr()

    for file in files:
        if os.path.isdir(file):
            print("暂不支持目录上传！")
            sys.exit(0)
        if os.path.isfile(file):
            suffix = os.path.splitext(file)[1][1:]
            prefix = "img/" if suffix in img_suffix else "file/"
            prefix += timeStr
            name = os.path.split(file)[1]
            up_filename = prefix + name
            ret, info, url = q.upload_file(bucket, up_filename, file)
            print("已上传： %s " % name)
            res += transform(name, url)
    print(res)  # 打印结果