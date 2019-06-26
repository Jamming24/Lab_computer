# -*- coding:utf-8 -*-
import re
import numpy
import scipy.stats as st
import numpy as np
import argparse
import math
import sys
import os
from numpy import *
# 这个模块是得到与wordsim里的单词对对应的单词向量的余弦值得列表，和wordsim里的评分列表。
# 这个方法调节为了调节词向量和词内部向量这两部分的权重
def merge_vector_method(weights, word_vector,merge_internal_vector):
    merge_word_vector = (1-weights)*word_vector + weights *merge_internal_vector
    return merge_word_vector
# 这个方法是计算两个向量的余弦值，同时把余弦正规化到0到5的区间内
def vector_weight_score(word1,word2):
    vec1 = numpy.array(word1)
    vec2 = numpy.array(word2)
    num = float(numpy.sum(vec1*vec2))
    denom = numpy.linalg.norm(vec1)*numpy.linalg.norm(vec2)
    cos = num/denom
    # score = ((cos+1)/2)*5
    return cos
# 这个计算內积的方法
def vector_inner_score(word1,word2):
    vec1 = mat(word1)
    vec2 = mat(word2)
    inner_number = vec1*vec2.T
    return float(inner_number)

# 1.欧式距离：源自欧式空间中两点间的距离公式。d=((x1-x2)^2+(y1-y2)^2)^(1/2)
def Euclidean(vec1, vec2):
    vec1 = np.mat(vec1)
    vec2 = np.mat(vec2)
    # score1 = np.sqrt((vec1 - vec2) * (vec1 - vec2).T)  # 输出是向量
    score2 = np.power(np.sum(np.power(np.abs(vec1 - vec2), 2)), 1 / 2)  # 输出是标量，与上面值一样
    # print(score2)
    return score2

#这个方法是的一行里词对应的词向量
def get_word_vector(line):
    word_vector =[]
    word_vector_list = line.split(' ')
    number = 0
    for i in word_vector_list:
        if number != 0:
            word_vector.append(float(i))
        number= number+1
    return word_vector

# 这个是判断词中是否含有不是中文的字符，如果含有不是中文字符，这返回ture，否则返回false
def is_all_english(s):
    for c in s:
        if not ('\u4e00' <= c <= '\u9fa5'):
            return True
    return False
def change_word_order(word):
    if is_all_english(word):
        return word
    else:
        return "".join(reversed([i for i in word]))

if __name__ == '__main__':
    read_evaluate_file = open("C:\\Users\\Jamming_Lab\Desktop\\词向量评价程序\\297.txt", 'r', encoding='utf-8')
    read_word_vector_file = open("F:\\迅雷下载\\add_component_word_vector.txt", 'r', encoding='utf-8')
    # write_file = open(r'D:\xiaoruiming\词向量的特征\对词语向量的余弦和欧式距离.txt', 'w', encoding='utf-8')
    # 这个列表中存储的每一行的词和其向量
    list_word_vecter = []
    list_word =[]
    model_score_list = []
    man_score_list = []
    number =1
    for line in read_word_vector_file:
        line_list = line.split(' ')
        # print(line)
        list_word_vecter.append(line)
        list_word.append(line_list[0].strip())
    for line in read_evaluate_file:
        line_list = line.split('\t')
        if line_list[0].strip() in list_word and line_list[1].strip() in list_word:

            #这行代码是通过词的列表list_word来获得wordsim297文件里词在词向量列表list_word_vecter中的位置
            vec1 = get_word_vector(list_word_vecter[list_word.index(line_list[0].strip())])
            vec2 = get_word_vector(list_word_vecter[list_word.index(line_list[1].strip())])
            # print(model_score)
            # print(man_score)
            # 这个是计算向量余弦的方法
            # print(line.strip("\n")+"\t"+str(vector_weight_score(vec1,vec2)))
            model_score_list.append(vector_weight_score(vec1, vec2))
            # 这个计算两个列表的內积
            # print(line.strip("\n")+"\t"+str(vector_inner_score(vec1,vec2)))
            # model_score_list.append(vector_inner_score(vec1,vec2))

            #欧式距离
            # print(line.strip("\n") + "\t" + str(Euclidean(vec1, vec2)))
            # model_score_list.append(Euclidean(vec1, vec2))

            man_score_list.append(float(line_list[2]))
        else :
            print(line.strip())
    # print(model_score_list)
    # print(man_score_list)
    print(len(model_score_list))
    # print(len(man_score_list))
    # 这个是求其spearman的得分
    rho, p_val = st.spearmanr(model_score_list, man_score_list)
    print(rho)

