# encoding:utf-8

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.externals import joblib
from sklearn.datasets import load_iris


def demo1():
    # 生成一个随机数据， 样本大小为100， 特征数为3
    data = np.random.rand(100, 3)
    print(data)
    # 构造聚类为3的聚类器
    estimator = KMeans(n_clusters=3)
    print(estimator)
    # 聚类
    estimator.fit(data)
    print(estimator)
    # 获取聚类标签
    label_pred = estimator.labels_
    print(label_pred)
    # 获取聚类中心
    centroids = estimator.cluster_centers_
    print(centroids)
    # 获取聚类总和准则
    inertia = estimator.inertia_
    print(inertia)


def demo2():
    num_clusters = 3
    '''
    n_clusters: 指定K的值
    max_iter: 对于单次初始值计算的最大迭代次数
    n_init: 重新选择初始值的次数
    init: 制定初始值选择的算法
    n_jobs: 进程个数，为-1的时候是指默认跑满CPU
    注意，这个对于单个初始值的计算始终只会使用单进程计算，
    并行计算只是针对与不同初始值的计算。比如n_init=10，n_jobs=40,
    服务器上面有20个CPU可以开40个进程，最终只会开10个进程

    '''
    km_cluster = KMeans(n_clusters=num_clusters, max_iter=300, n_init=40, init='k-means++', n_jobs=-1)
    #返回各文本所被分配到的索引
    result = km_cluster.fit_predict(tfidf_matrix)
    print("Predicting result: ", result)


def demo3():
    # 模型保存与载入
    # 注释语句用来存储你的模型
    joblib.dump(km, 'doc_cluster.pkl')
    km = joblib.load('doc_cluster.pkl')
    clusters = km.labels_.tolist()

    # 聚类类别统计
    frame = pd.DataFrame(films, index=[clusters], columns=['rank', 'title', 'cluster', 'genre'])
    frame['cluster'].value_counts()


def demo4():
    ##表示我们只取特征空间中的后两个维度
    X = load_iris().data[:, 2:4]
    print(X.shape)
    # 绘制数据分布图
    plt.scatter(X[:, 0], X[:, 1], c="red", marker='o', label='see')
    plt.xlabel('petal length')
    plt.ylabel('petal width')
    plt.legend(loc=2)
    plt.show()

    estimator = KMeans(n_clusters=3)  # 构造聚类器
    estimator.fit(X)  # 聚类
    label_pred = estimator.labels_  # 获取聚类标签
    # 绘制k-means结果
    x0 = X[label_pred == 0]
    x1 = X[label_pred == 1]
    x2 = X[label_pred == 2]
    plt.scatter(x0[:, 0], x0[:, 1], c="red", marker='o', label='label0')
    plt.scatter(x1[:, 0], x1[:, 1], c="green", marker='*', label='label1')
    plt.scatter(x2[:, 0], x2[:, 1], c="blue", marker='+', label='label2')
    plt.xlabel('petal length')
    plt.ylabel('petal width')
    plt.legend(loc=2)
    plt.show()


def staticalUserInfo(user_infos_file):
    count = 0
    file_object = open(user_infos_file, 'r', encoding='UTF-8')
    for line in file_object:
        t = line.split('\t')
        userID = t[0]
        frequency = t[3]
        if frequency == "daily":
            count += 1
    print(count)
#   2414515
    file_object.close()


def staticalPurity_Train_Set(purity_training_set_file):
    purity_training_set_object = open(purity_training_set_file, 'r', encoding='UTF-8')
    count = 0
    for line in purity_training_set_object:
        t = line.split('\t')
        if int(t[1]) > 160:
            count += 1
    print(count)
    purity_training_set_object.close()


if __name__ == '__main__':
    # demo4()
    # print(load_iris().data)
    user_infos_file = "E:\\CCIR\\user_infos.txt"
    purity_training_set_file = "E:\\CCIR\\purity_training_set.txt"
    # staticalUserInfo(user_infos_file)
    staticalPurity_Train_Set(purity_training_set_file)
