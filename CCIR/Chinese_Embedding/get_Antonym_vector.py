# -*- coding: UTF-8 -*-
import numpy as np
##用于可视化图表
import matplotlib.pyplot as plt
##导入PCA库
from sklearn.decomposition import PCA


def load_word_vector(words_set, vector_file):
    vetcor_file_object = open(vector_file, 'r', encoding='UTF-8')
    Antonym_Vector_dict = dict()
    flag = 0
    size = 0
    for line in vetcor_file_object:
        ll = line.strip("\n").split(" ")
        if flag == 0:
            flag = 1
            # 词数
            word_nums = line.split(' ')[0]
            print(f'总词数:{word_nums}')
            # 维度
            size = int(line.split(" ")[1])
            print(f"向量维度:{size}")
        else:
            character = ll[0]
            vector = ll[1:size + 1]
            if character in words_set:
                words_set.remove(character)
                Antonym_Vector_dict[character] = np.array(list(map(lambda x: float(x), vector)))
    vetcor_file_object.close()
    print(f"得到反义词向量总数:{len(Antonym_Vector_dict)}")
    print(words_set)
    for unkown_word in words_set:
        Antonym_Vector_dict[unkown_word] = np.zeros(size)
    return Antonym_Vector_dict


def load_Antonym_words(antonym_file):
    words_set = set()
    words_pairs = []
    antonym_file_object = open(antonym_file, 'r', encoding='UTF-8')
    for line in antonym_file_object:
        word_pairs = line.strip('\n')
        word_one = word_pairs[:2]
        word_two = word_pairs[2:]
        words_set.add(word_one)
        words_set.add(word_two)
        words_pairs.append(word_pairs)
    antonym_file_object.close()
    print(f"反义词数量:{len(words_set)}")
    print(f"反义词对数:{len(words_pairs)}")
    return words_set, words_pairs


def print_antonym_vector(Word_pairs, Antonym_Vector_dict, Antonym_vector_file):
    antonym_vector_file_object = open(Antonym_vector_file, 'w', encoding='UTF-8')
    for word in Word_pairs:
        antonym_vector_file_object.write(word+"\n")
        antonym_vector_file_object.write(word[:2] + " ")
        for w1 in Antonym_Vector_dict[word[:2]]:
            antonym_vector_file_object.write(str(round(w1, 6)) + " ")
        antonym_vector_file_object.write("\n")

        antonym_vector_file_object.write(word[2:] + " ")
        for w1 in Antonym_Vector_dict[word[2:]]:
            antonym_vector_file_object.write(str(round(w1, 6)) + " ")
        antonym_vector_file_object.write("\n")
    antonym_vector_file_object.close()
    print("向量打印完成")


def test_PCA(Antonym_Vector_dict):
    Antonym_Vector_list = list()
    word_list = list()
    for key in Antonym_Vector_dict.keys():
        word_list.append(key)
        Antonym_Vector_list.append(Antonym_Vector_dict[key])
    print(len(word_list))
    print(len(Antonym_Vector_list))
    Antonym_Vector_matrix = np.matrix(Antonym_Vector_list)
    # print(Antonym_Vector_matrix)

    # iris = datasets.load_iris()
    # iris_X = iris.data
    # iris_Y = iris.target
    # print(iris_X.shape) # 显示共有150个样本，每个样本四个特征
    # print(iris.feature_names)
    # print(iris.target_names)

    model_pca = PCA(n_components=2)
    X_pca = model_pca.fit(Antonym_Vector_matrix).transform(Antonym_Vector_matrix)
    print(X_pca.shape)
    print(X_pca)
    # print("降维后的各个方向:\n", model_pca.components_)
    # print("降维后各主成分的差值：", model_pca.explained_variance_)
    # print("降维后各主成分的方差与总方差之比：", model_pca.explained_variance_ratio_)
    # print("奇异值分解后的特征值：", model_pca.singular_values_)
    # print("降维后的主成分:", model_pca.n_components)

    print(">>>>>>"+str(len(X_pca[:, 0])))
    print(X_pca[:, 0])
    print("<<<<<<"+str(len(X_pca[:, 1])))
    print(X_pca[:, 1])
    # plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.plot(X_pca[:, 0], X_pca[:, 1], c='r')
    # for i in range(1, 250):
        # plt.annotate(word_list[i], xy=(X_pca[i:, 0], X_pca[i:, 1]), xytext=(X_pca[i:, 0]+0.1, X_pca[i:, 1]+0.1))
        # plt.text(X_pca[i:, 0], X_pca[i:, 1], "a")
    plt.show()


if __name__ == '__main__':
    antonym_file = "F:\\迅雷下载\\反义词表.txt"
    vector_file = "F:\\迅雷下载\\学习率为0.015且min_count为7的按词分割的总语料.vector"
    antonym_vector_file = "F:\\迅雷下载\\125对反义词向量.txt"
    # 加载反义词表和 反义词对
    words_set, words_pairs = load_Antonym_words(antonym_file)
    # 加载反义词向量
    antonym_Vector_dict = load_word_vector(words_set, vector_file)
    # 打印向量
    # print_antonym_vector(words_pairs, antonym_Vector_dict, antonym_vector_file)
    # 画图
    test_PCA(antonym_Vector_dict)
