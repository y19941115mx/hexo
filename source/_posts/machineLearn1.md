---
title: 机器学习入门—以k近邻算法为例
date: 2018-11-01 22:18:06
tags: [机器学习, KNN算法]
---
> k 近邻算法是机器学习中最基础的分类算法，基本思想是使用距离测量的方法对样本进行分类，非常有效而且易于掌握。本章节的学习目标：在学习KNN算法思想的同时，掌握sklearn机器学习库的使用和机器学习的基本知识。
<!-- more -->
## 工作原理
k 近邻算法的工作原理：存在一个样本数据集集合，并且该集合中每个数据都存在标签，即我们知道样本集合中每一个数据所属的分类。当输入一个没有标签的新数据后，根据新数据的各个特征与样本集合中的数据进行比较，使用计算距离的算法（欧拉距离等），提取出前k个与输入数据最相似（最近邻）的样本数据，选择样本数据中出现次数最多的标签，作为新数据的标签。对没有标签的数据进行预测，从而实现一个简单的分类器。
## 实现流程
使用一个机器学习算法的一般流程，如下图所示：
![](https://ws1.sinaimg.cn/large/006tNbRwly1fwsxeobd72j30y805mq4r.jpg)

### 收集数据 与 分析数据

数据的整体被称作一个数据集（DataSet）
每一行数据 称作 一个样本
每一行的最后一列称作样本的标记 其余列为样本的特征 
样本的数个特征组成特征向量**X** 把特征作为变量可以表示一个特征空间。 分类任务的本质就是对特征空间的切分
特征不一定都具有语意，它可以很抽象，例如使用像素点。
![数据举例](https://upload-images.jianshu.io/upload_images/9531730-92160184cf4e80c0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**收集数据** 就是把各种形式的源数据，经过数据预处理过程，统一处理成计算机易处理的形式，例如数据库、文件等

**分析数据** 是将数据进行简单的可视化和数据分析，从何初步确定使用哪一种机器学习的算法

为了评估生成的模型 一般会对收集的数据集进行一次数据集划分，如下图：

![](https://ws4.sinaimg.cn/large/006tNbRwly1fwsxfs9wo4j30ok09wmzu.jpg)

使用sklern库实现

```python
from sklearn.datasets import load_iris

data = load_iris() # 载入鸢尾花测试数据

X, y = data.data, data.target # 对应数据的特征矩阵和标记向量



from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X,y) # 对数据集进行划分
```

### 训练模型
使用训练数据集，根据机器学习的算法生成对应的模型, 一般认为KNN是没有模型的机器学习算法，sklearn为了统一接口，将训练数据集本身当做KNN算法的模型，训练数据本身直接影响KNN算法的效果，所以在使用knn算法时，要特别注意数据的归一化处理，消除不同特征单位造成的影响。代码实现如下：

```python
# 数据的归一化
from sklearn.preprocessing import StandardScaler, Normalizer # 均值方差归一化与均值归一化

scaler = StandardScaler()

scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test) # 注意 测试数据也要使用同一个归一化对象进行归一化

# 训练模型
from sklearn.neighbors import KNeighborsClassifier
knn_clf = KNeighborsClassifier() # 这里使用默认的超参数初始化KNN分类器
knn_clf.fit(X_test, y_test) # 训练模型 对应于KNN算法 是将归一化后的训练数据传入分类器对象
knn_clf.predict(x_test) # 对训练数据集的样本进行预测分类
knn_clf.score(X_test, y_test) # 直接获取模型在测试集上对应的正确率

```

### 测试模型与调参
不同的机器学习算法对应不同的超参数，在sklearn库中提供了网格搜索法，对不同超参数进行组合，在生成的不同模型间进行测试和比较，选出准确率最高的模型，给调参带来便利。代码实现如下：
```python
from sklearn.model_selection import GridSearchCV
# 使用字典 或 字典列表生成网格搜索的参数
grid_params = [{
    'n_neighbors': [i for i in range(1,10)], # 代表 K 的值
    'weights': ['uniform'], # 是否考虑距离的权重 uniform为不考虑
     'p': [ i for i in range(1, 5)] # 米可夫斯基距离的 P 代表使用不同的距离测量公式（1为曼斯顿距离，2为欧拉距离）
},{
     'n_neighbors': [i for i in range(1, 10)],
    'weights':['distance'],
    'p': [ i for i in range(1, 5)]
}
]
# 使用网格搜索寻找最好的模型
grid_cv = GridSearchCV(knn_clf, grid_params, n_jobs=-1, verbose=2)
grid_cv.fit(X_train, y_train) # 传入归一化后的训练数据

grid_cv.best_score_ # 获取网格搜索下最好的预测正确率
grid_cv.best_estimator_ 获取网格搜索下最好的模型
grid_cv.best_params_ # 获取网格搜索下最好的模型对应的参数

```
## 小结
k近邻算法是分类任务中最简单和有效的算法，但在使用该算法时 需要保存全部的训练数据集 计算的时间也随数据规模迅速增长，数据量大的时候 可能会非常耗时，而且KNN算法给出的分类结果不具备解释性，我们无法学习到数据背后蕴含的知识和规律。本章的学习，算法部分很简单，主要是想让读者对机器学习中一些基本的概念，算法的一般流程有个大致印象，了解sklearn库的整体使用方式。
