---
title: 常用编程工具（Mac）
date: 2018-10-01 22:06:26
tags: 编程工具
---
> 俗话说得好，“磨刀不误砍柴功”，选择合适的编程工具，能够帮助开发人员更加高效的进行代码编辑，协助开发人员进行版本控制、代码测试和源码读取，在开发的过程中，极大地提高我们的工作效率。这里介绍几款常用的编程工具。
<!--more-->
### pycharm：高富帅
pycharm是JetBrains公司推出的一款python的集成开发工具，“JetBrains出品，必属精品”，几乎所有编程语言，都能找到该公司开发的对应IDE，这里拿pycharm举例，列举几个开发中常用到的功能和快捷键，对于他们家其他的IDE基本是通用的。

1. 添加注释 使用三个双引号然后回车 可以自动生成备注
2. 查看源码 cmd + click on anyywhere
3. 格式化代码 Command+Option+L
4. Command + J 插入常用代码
5. Command+P 可以显示出光标处函数参数
6. 分栏操作 右键文件名 点击split 
7. cmd + shift +o 搜索文件并打开 
8. shift * 2  Search Everywhere 不仅是文件名包括函数名或者变量
9. cmd + shift + T 为当前的函数生成单元测试类 常用的是self.assertEqual()进行测试
10. vcs工具栏 进行git版本控制 常用是commit(提交) revert(撤销修改) reset(撤销版本)操作 注意revert和同名的git命令略有不同这里是撤销修改。
11. Tool菜单的Deployment 配置远程服务器 进行ssh远程部署
12. command + d 直接复制一行 
13. option + shift + 上下 移动代码

### sublime：经济适用型
拥有记事本的打开速度，配合丰富的插件，使得文本编辑器也能拥有接近IDE的开发体验，是快速开发程序的利器。
#### 常用快捷键
快捷键 | 功能
:---:|---
cmd + d | 多行操作 常用于多行替换
cmd + f | 查找文件 支持正则
cmd + r | 文件替换，需要修改快捷键
cmd + i | 格式化选中的代码，需要修改快捷键
cmd + shift + f | 全局查找、替换 支持正则
cmd + p | 查找文件 使用@ 查找当前文件的结构
cmd +shift + p | 呼出功能菜单
cmd + B | 直接编译(python编译请使用默认的Python 使用Anaconda会有中文乱码问题)

#### 插件安装
subliem只有配合使用各种插件 才能发挥出真正的功效，这里列举几个我在开发中经常用到的插件，至于sublime怎么安装插件大家可以自行百度。

1. AdvancedNewFile插件 cmd + n快速新建文件
2. anaconda_python 支持python 大家可以对应自己经常使用的编程语言下载对应的插件 例如经常做微信小程序开发，可以下载wxapp插件。
3. side bar 增强边栏功能 f2用浏览器打开文件
4. all Autocomplete 会搜索所有打开的文件来寻找匹配的提示词
5. sftp 远程部署工具
6. HTML-css-js prttity 右键就可以快速格式化html,css,js代码
7. terminal 插件 shift +command + T 在当前文件夹打开命令行
9. Markdown Editing  Markdown的语法高亮提醒
10. Color Highlighter 显示颜色功能
11. AutoFileName 快速帮助你在文件中写路径

#### 配置
```bash
// 全局setting
"tab_size": 4,

"translate_tabs_to_spaces": true

// anaconda setting
{

"python_interpreter": "python安装位置/python.exe",

"suppress_word_completions":true,

"suppress_explicit_completions":true,

"complete_parameters":true,

"anaconda_linting": false

}

//全局key Binding
[ 
    { "keys": ["f2"], "command": "side_bar_files_open_with",
            "args": {
                "paths": [],
                "application": "/Applications/Google Chrome.app",
                "extensions":".*"
            }
     },
     {
        "command": "anaconda_doc", "keys": ["alt+/"], "context": [
            {"key": "selector", "operator": "equal", "operand": "source.python"}
        ]
    },
    {"keys": ["ctrl+i"], "command": "reindent" , "args":
    {"single_line": false}},
    { "keys": ["super+n"], "command": "advanced_new_file_new" },
    { "keys": ["super+r"], "command": "show_panel", "args": {"panel": "replace", "reverse": false} },

]
```
#### emmet语法
子代 >生成层级关系

> div>ul>li{标签内的内容}

兄弟 + 生成并列关系
> div+ul +li

父代^
> li^div 生成父节点

重复: *次数

成组:（）

id: #idnum

class: .classname

属性: [name="hello"]

### vi：编辑器之神
万能编辑器，编辑器界的王者，Linux下最好用的编辑器。首先在用户目录下编辑自己的.vimrc文件，进行相关配置。
```bash
let python_highlight_all=1
syntax on
set encoding=utf-8
set number
set tabstop=4
set softtabstop=4
set shiftwidth=4
set textwidth=79
set expandtab
set autoindent
set fileformat=unix

```
#### 常用快捷键
快捷键 | 操作
:---:|---
control + f(b) | 翻页
o（O）| 光标来到下一行（上一行）
a(A) | 光标来到行首和行末 
:1 | 光标来到首行
:$ | 光标来到最后行
/xxx | 向后搜索字符串
?xxx | 向前搜索字符串（n 下一个）
(n,$) s/vivi/sky/g | 替换n行开始到最后 每一个的str1为str2
sp fileName | 分栏新建文件 ctrl + w 切换文件
r name  | 读取文件到当前文件
行数 + dd | 从光标所在位置开始剪切几行
yy | 复制行
p | 粘贴
x | 删除
u |撤销上步操作
!+shell命令 | 执行shell命令后返回vim
*例如：!python name 编译python程序*

### jupyterNoteBook
既满足交互性，又具备可读性，jupyterNoteBook是python进行机器学习和数据炼金术的常用工具 它的快捷键在首页就有提示。这里只列举几个常用的魔法命令
#### 常用魔法命令
快捷键 | 操作
---|---
% run | 执行脚本，并且可以在ipython中使用该脚本中的变量
%time | 执行**一条**语句所需要的时间（%timeit 更精确）
%%time | 可以测试一个函数体所需要的时间
