---
title: 常用编辑器 快捷键（Mac）
tags: 编程工具
---
# pycharm
0. 关于注释 使用三个双引号 然后回车
1. 查看使用库源码：cmd + click on anyywhere
2. 格式化代码 Command+Option+L
3. Command + J ，就可以直接插入常用代码了
<!--more-->
4. Command+P 可以显示出光标处函数参数。
5. 分栏操作 右键文件名 split 
6. cmd + shift +o 打开文件 Search Everywhere 两次 shift 不仅是文件名包括函数名或者变量
7. 可以在navigate栏中 选中对应的类来生成单元测试文件
8. 图形化 VCS 操作git 在vcs工具栏中使用
9. ssh远程部署 Tool菜单的Deployment 配置远程服务器
10. command + d 直接复制一行
11. alt + shift + 上下 移动代码

![快捷键.jpg](https://upload-images.jianshu.io/upload_images/9531730-ba94c774f8c62a27.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# sublime
**快捷键**：

快捷键 | 功能
:---:|---
command + ctrl + 上下键| 移动代码
ctrl +d | 选中标签内的内容
command+d | 多行操作
shift +command +d | 直接复制该行
alt + command + 1 or 2 | 开启关闭分栏模式
cmd + p | 查找文件
cmd +shift + p | 呼出功能菜单

**插件安装**

```
1. AdvancedNewFile插件

2. anaconda_python 支持python操作 
// package setting

{

"python_interpreter": "python安装位置/python.exe",

"suppress_word_completions":true,

"suppress_explicit_completions":true,

"complete_parameters":true,

"anaconda_linting": false

}

3. side bar 增强边栏功能
4. all Autocomplete与better completion(需要配置) 实现代码自动补全提示
5. sftp 服务器上传工具

6. HTML/css/js prttity 右键就可以找到快速格式化html,css,js代码

7. terminal 插件
shift +command + T 在当前文件夹打开命令行

8. bs3-snipit

[https://github.com/JasonMortonNZ/bs3-sublime-plugin](https://github.com/JasonMortonNZ/bs3-sublime-plugin)

9. Markdown 支持
Markdown Editing 
```

**sublime常用设置**
```
// 全局setting

"tab_size": 4,

"translate_tabs_to_spaces": true

//全局key Binding

[

//chrome

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

// 自动对齐

{"keys": ["ctrl+i"], "command": "reindent" , "args":

{"single_line": false}},

{ "keys": ["super+n"], "command": "advanced_new_file_new" }

]
```

**emmet 语法**

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

# vi 的配置与使用
保存到自己的.vimrc
```
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

vi编辑器：

快捷键 | 操作
---|:---:
control + f(b)  | 翻页
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

# ipython（jupyterNoteBook）
常用魔法命令

快捷键 | 操作
---|---
% run| 执行脚本，并且可以在ipython 中使用该脚本中的变量
%time | 执行**一条**语句所需要的时间（%timeit 更精确）
%%time | 可以测试一个函数体所需要的时间
