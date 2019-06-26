# -*- coding: UTF-8 -*-

import numpy as np
from CCIR.Chinese_Embedding import Experiment_BasedOn_Component as ebc
from CCIR.Chinese_Embedding import Strokes_number as sn


def get_component_set():
    component_set = set()
    component_dict = ebc.read_all_component()
    for chara in component_dict.keys():
        for comp in component_dict[chara]:
            component_set.add(comp)
    print(f"总计汉字组件个数：{len(component_set)}")
    return component_set, component_dict


def load_component_and_word_vector(wiki_with_component_vector_file, Component_set, words):
    # 加载 含有部首向量和词向量混合向量文件
    file_object = open(wiki_with_component_vector_file, 'r', encoding='UTF-8')
    Component_Vector = dict()
    Word_Vector = dict()
    flag = 0
    Size = 0
    for line in file_object:
        ll = line.strip("\n").split(" ")
        if flag == 0:
            flag = 1
            # 词数
            word_nums = ll[0]
            print(f'文件包含向量总数量:{word_nums}')
            # 维度
            Size = int(ll[1])
            print(f"向量维度:{Size}")
        elif ll[0] in Component_set:
            vector = ll[1:Size + 1]
            Component_Vector[ll[0]] = np.array(list(map(lambda x: float(x), vector)))
        elif ll[0] in words:
            vector = ll[1:Size + 1]
            Word_Vector[ll[0]] = np.array(list(map(lambda x: float(x), vector)))
    file_object.close()
    print(f"词向量个数:{len(Word_Vector)}")
    print(f"组件向量个数:{len(Component_Vector)}")
    return Component_Vector, Word_Vector, Size


def Component2Character_withOut_weight(component_vectors, Components_dict, words, vector_size):
    # 将组件向量加和成为汉字向量
    Character_vectors = dict()
    character_set = set()
    for word in words:
        for chara in word:
            character_set.add(chara)
    print(f"汉字总数{len(character_set)}")
    for ch in character_set:
        if ch in Components_dict.keys():
            component_list = Components_dict[ch]
            sum_component_vector = np.zeros(vector_size)
            for component in component_list:
                sum_component_vector += component_vectors[component]
            # 组件向量总和除以组件个数，表示汉字向量
            sum_component_vector = sum_component_vector/len(component_list)
            Character_vectors[ch] = sum_component_vector
    return Character_vectors


if __name__ == '__main__':
    wiki_with_component_file = "F:\\迅雷下载\\simply_wiki_with_component_vector.txt"
    word_file = "F:\\迅雷下载\\Words.txt"
    outfile = "F:\\迅雷下载\\update_simply_wiki_with_component_vector.txt"
    Words = ebc.load_Words(Words_file=word_file)
    component_set, component_dict = get_component_set()
    component_vector, word_vector, size = load_component_and_word_vector(wiki_with_component_file, component_set, Words)
    character_vectors = Component2Character_withOut_weight(component_vector, component_dict, Words, size)
    update_wordvector_dict = sn.Character2Words(character_vectors, word_vector, Words)
    sn.Print_update_WordVector(update_wordvector_dict, outfile, size)

