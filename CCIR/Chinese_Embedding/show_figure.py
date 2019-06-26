# -*- coding: UTF-8 -*-

##用于3D可视化
# from mpl_toolkits.mplot3d import Axes3D
##用于可视化图表
import matplotlib.pyplot as plt
##用于做科学计算
import numpy as np
##用于做数据分析
import pandas as pd
# 用于加载数据或生成数据等
from sklearn import datasets
##导入PCA库
from sklearn.decomposition import PCA
##导入LDA库
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


def test_PCA():
    iris = datasets.load_iris()
    iris_X = iris.data
    iris_Y = iris.target
    print(iris_X.shape) # 显示共有150个样本，每个样本四个特征
    print(iris.feature_names)
    print(iris.target_names)

    model_pca = PCA(n_components=2)
    X_pca = model_pca.fit(iris_X).transform(iris_X)
    print(iris_X.shape)
    print(iris_X[0:5])
    print(X_pca.shape)
    print(X_pca[0:5])
    print("降维后的各个方向:\n", model_pca.components_)
    print("降维后各主成分的差值：", model_pca.explained_variance_)
    print("降维后各主成分的方差与总方差之比：", model_pca.explained_variance_ratio_)
    print("奇异值分解后的特征值：", model_pca.singular_values_)
    print("降维后的主成分:", model_pca.n_components)

    fig = plt.figure(figsize=(10, 8))
    plt.scatter(X_pca[:, 0], X_pca[: 1], marker='o', c=iris_Y)
    plt.show()




