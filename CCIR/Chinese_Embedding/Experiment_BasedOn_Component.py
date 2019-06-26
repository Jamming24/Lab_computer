# -*- coding: UTF-8 -*-

import numpy as np


def load_Words(Words_file):
    WordS_object = open(Words_file, 'r', encoding="UTF-8")
    words = set()
    # 得到词表
    for word in WordS_object:
        words.add(word.strip('\n'))
    WordS_object.close()
    print(f"总词数:{len(words)}")
    return words


def read_all_component():
    component_dict = {}
    file_object = open("C:\\Users\\Jamming_Lab\\Desktop\\汉字部首\\汉字组件表.txt", 'r', encoding='UTF-8')
    for line in file_object:
        t = line.strip('\n').split('\t')
        component_dict[t[0]] = t[1]
    file_object.close()
    print(f"加载部首数量:{len(component_dict)}")
    return component_dict


def combine_component_vector(component_Vector_file, character_Vector_file, word_vector_file, Words):
    component_dict = read_all_component()
    component_vector_object = open(component_Vector_file, 'r', encoding="UTF-8")
    Character_Vector_object = open(character_Vector_file, 'w', encoding="UTF-8")
    Word_Vector_object = open(word_vector_file, 'w', encoding="UTF-8")

    component_vectors = dict()
    size = 0
    for line in component_vector_object:
        ll = line.strip("\n").split(" ")
        character = ll[0]
        size = len(ll) - 2
        vector = ll[1:-1]
        new_vector = np.array(list(map(lambda x: float(x), vector)))
        component_vectors[character] = new_vector

    character_vectors = dict()
    Words_vectors = dict()

    for word in Words:
        sum_character_vector = np.zeros(size)
        for ch in word:
            if ch in component_dict.keys():
                component_list = component_dict[ch]
                sum_component_vector = np.zeros(size)
                for component in component_list:
                    sum_component_vector += component_vectors[component]
                # 组件向量总和除以组件个数，表示汉字向量
                sum_component_vector = sum_component_vector/len(component_list)
                character_vectors[ch] = sum_component_vector
                sum_character_vector += sum_component_vector
        Words_vectors[word] = sum_character_vector/len(word)
    Character_Vector_object.write(str(len(character_vectors)) + " " + str(size) + "\n")

    for ch in character_vectors.keys():
        Character_Vector_object.write(ch + " ")
        for n in character_vectors[ch]:
            Character_Vector_object.write(str(round(n, 6)) + " ")
        Character_Vector_object.write("\n")

    Word_Vector_object.write(str(len(Words)) + " " + str(size) + "\n")
    for word in Words_vectors.keys():
        Word_Vector_object.write(word + " ")
        for w in Words_vectors[word]:
            Word_Vector_object.write(str(round(w, 6)) + " ")
        Word_Vector_object.write("\n")

    Word_Vector_object.close()
    component_vector_object.close()
    Character_Vector_object.close()
    return Words_vectors


def combine_Word_Component_vector(word_vector_file, Words_vectors, new_word_vectors_file, Words):
    new_word_vectors_object = open(new_word_vectors_file, 'w', encoding='UTF-8')
    word_vector_object = open(word_vector_file, 'r', encoding='UTF-8')
    new_word_vectors = dict()
    size = 0
    for line in word_vector_object:
        # 用gensim生成的要加上strip(\n)
        ll = line.strip('\n').split(" ")
        character = ll[0]
        if character in Words:
            vector = ll[1:-1]
            # print(character)
            # print(vector)
            # print(len(vector))
            new_vector = np.array(list(map(lambda x: float(x), vector)))
            # if character in Words_vectors.keys():
            sum_vector = new_vector + Words_vectors[character]
            size = len(sum_vector)
            new_word_vectors[character] = sum_vector/2
            # Words_vectors.pop(character)

    # 补足词表
    # for ex_word in Words_vectors.keys():
    #     new_word_vectors[ex_word] = Words_vectors[ex_word]

    new_word_vectors_object.write(str(len(new_word_vectors)) + " " + str(size) + "\n")
    for word in new_word_vectors.keys():
        new_word_vectors_object.write(word + " ")
        for w in new_word_vectors[word]:
            new_word_vectors_object.write(str(round(w, 6)) + " ")
        new_word_vectors_object.write("\n")

    word_vector_object.close()
    new_word_vectors_object.close()
    return new_word_vectors


if __name__ == '__main__':
    # component_vector_file = "F:\\迅雷下载\\wiki_component-update_vector.txt"
    # Character_Vector_file = "F:\\迅雷下载\\繁体_combine_component2character_update_Vector.txt"
    # Word_Vector_file = "F:\\迅雷下载\\繁体_combine_character2word_Vector.txt"
    # words_file = "F:\\迅雷下载\\繁体_Words.txt"
    # word_vector_file = "F:\\迅雷下载\\Ansj_Segment_wiki_vector.txt"
    # new_word_vectors_file = "F:\\迅雷下载\\繁体_add_component_Ansj_Segment_wiki_vector.txt"

    component_vector_file = "F:\\迅雷下载\\simply_wiki_component_corpus_vector_gensim.text"
    Character_Vector_file = "F:\\迅雷下载\\simply_wiki_combine_component2character_Vector_gensim.txt"
    Word_Vector_file = "F:\\迅雷下载\\simply_wiki_combine_character2word_Vector_gensim.txt"
    words_file = "F:\\迅雷下载\\Words.txt"

    word_vector_file = "F:\\迅雷下载\\Segment_simply_wiki.zh_corpus_vector_gensim.text"
    new_word_vectors_file = "F:\\迅雷下载\\simply_wiki_add_component_Ansj_Segment_wiki_vector_gensim.txt"

    Words = load_Words(words_file)
    Words_vectors = combine_component_vector(component_vector_file, Character_Vector_file, Word_Vector_file, Words)
    combine_Word_Component_vector(word_vector_file, Words_vectors, new_word_vectors_file, Words)
    print("计算完成")
