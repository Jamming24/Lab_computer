'''
旨在总结一下各种相似度计算，分两大类：输入是向量 和 输入是字符串
'''

'''
首先，输入是两个向量
'''
import numpy as np


# 1.欧式距离：源自欧式空间中两点间的距离公式。d=((x1-x2)^2+(y1-y2)^2)^(1/2)
def Euclidean(vec1, vec2):
    vec1 = np.mat(vec1)
    vec2 = np.mat(vec2)
    # score1 = np.sqrt((vec1 - vec2) * (vec1 - vec2).T)  # 输出是向量
    score2 = np.power(np.sum(np.power(np.abs(vec1 - vec2), 2)), 1 / 2)  # 输出是标量，与上面值一样
    print(score2)
    return score2


# 2.曼哈顿距离 城市街区距离，非两点间的直线距离。 d=|x1-x2|+|y1-y2|
def Manhattan(vec1, vec2):
    vec1 = np.mat(vec1)
    vec2 = np.mat(vec2)
    score = np.sum(np.abs(vec1, vec2))
    print(score)
    return score


# 3.切比雪夫距离 max（|x2-x1|,|y2-y1|）
def Chebushev(vec1, vec2):
    vec1 = np.mat(vec1)
    vec2 = np.mat(vec2)
    score = np.max(np.abs(vec1 - vec2))
    print(score)
    return score


# 4.闵可夫斯基距离  闵氏距离不是一种距离,而是一组距离的定义
# d = ((x1-y1)^p+(x2-y2)^p)^(1/p)
'''
这里p是一个变参数,这里仅取p从1-10
p=1时就是曼哈顿距离
p=2时就是欧式距离
p->无穷就是切比雪夫距离
闵氏距离缺点主要有两个：
（1）将各个分量的量纲（scale）,也就是单位当做相同的看待。
（2）没有考虑各个分量的分布（期望，方差）可能是不同的。
'''


def Minkowski(vec1, vec2):
    vec1 = np.mat(vec1)
    vec2 = np.mat(vec2)
    feas = []
    for p in range(1, 10):
        if p == 1:
            score = np.sum(np.abs(vec1 - vec2))
            feas.append(score)
            print(p, score)
            # pass
        else:
            score = np.power(np.sum(np.power(np.abs(vec1 - vec2), p)), 1 / p)
            feas.append(score)
            print(p, score)
            # score = np.max(np.abs(vec1 - vec2))


# 5.标准化欧式距离（Standardized Euclidean distance）
'''
标准化欧氏距离是针对简单欧氏距离的缺点而作的一种改进方案。
标准欧氏距离的思路：既然数据各维分量的分布不一样，好吧！那我先将各个分量都“标准化”到均值、方差相等吧
'''
def StandarEuclidean(vec1, vec2):
    vec1 = np.mat(vec1)
    vec2 = np.mat(vec2)

    # vstack()函数  函数原型：vstack(tup) ，参数tup可以是元组，列表，或者numpy数组，返回结果为numpy的数组
    # 作用：在垂直方向把元素堆叠起来
    X = np.vstack([vec1, vec2])
    sk = np.var(X, axis=0, ddof=0)  # 方差

    # 方法一：根据公式求解
    # print('sk',sk)
    d1 = np.sqrt(((np.power((vec1 - vec2), 2) / sk).sum()))
    # print('d1',d1)

    # 方法二：根据scipy库求解
    # from scipy.spatial.distance import seuclidean
    # d3 = seuclidean(vec1, vec2, sk)
    # print('d3',d3)
    return d1

# 6.cos余弦
def Cosin_distance(vec1,vec2):
    import math
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    res = vec1.dot(vec2)/(math.sqrt((vec1**2).sum()) * math.sqrt((vec2**2).sum()))
    print(vec1.dot(vec2))
    print(res)
    return res


'''
然后，输入是两个字符列表
'''
# 1.jaccard系数
def jaccard(str1, str2):
    # com = [i for i in str1 if i in str2]
    # print(com)
    com = []
    len1 = len(str1)
    len2 = len(str2)
    for x in str1:
        if x in str2:
            com.append(x)
            str2.remove(x)
    # dis2 = [i for i in str1 if i not in str2]
    # print('dis2',dis2)
    score = float(len(com))/(len1+len2-len(com))
    print(score)
    return score
# 2.編輯距離
# 针对列表改写的编辑距离，在NLP领域中，计算两个文本的相似度，是基于句子中词和词之间的差异。
# 如果使用传统的编辑距离算法，则计算的为文本中字与字之间的编辑次数。这里根据编辑距离的思维，
# 将编辑距离中的处理字符串中的字符对象，变成处理list中每个元素
def Edit_distance_array(str_ary1, str_ary2):
    len_str_ary1 = len(str_ary1) + 1
    len_str_ary2 = len(str_ary2) + 1
    matrix = [0 for n in range(len_str_ary1 * len_str_ary2)]
    for i in range(len_str_ary1):
        matrix[i] = i
    for j in range(0, len(matrix), len_str_ary1):
        if j % len_str_ary1 == 0:
            matrix[j] = j // len_str_ary1
    for i in range(1, len_str_ary1):
        for j in range(1, len_str_ary2):
            if str_ary1[i-1] == str_ary2[j-1]:
                cost = 0
            else:
                cost = 1
            matrix[j*len_str_ary1+i] = min(matrix[(j-1)*len_str_ary1+i]+1, matrix[j*len_str_ary1+(i-1)]+1, matrix[(j-1)*len_str_ary1+(i-1)] + cost)
    distance = int(matrix[-1])
    similarity = 1-int(matrix[-1])/max(len(str_ary1), len(str_ary2))
    print('Distance:', distance, '\tSimilarity:', similarity)
    return {'Distance': distance, 'Similarity': similarity}
if __name__ == '__main__':
    vec1 = [3, 2,4]
    vec2 = [-3, 2,5]

    # Euclidean(vec1, vec2)
    # Manhattan(vec1, vec2)
    # Minkowski(vec1, vec2)
    # StandarEuclidean(vec1, vec2)
    # jaccard(vec1, vec2)
    # Cosin_distance(vec1,vec2)
    Edit_distance_array(vec1,vec2)