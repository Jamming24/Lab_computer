# -*- coding: UTF-8 -*-

from CCIR.Chinese_Embedding import Experiment_BasedOn_Component as ebc
import numpy as np


def read_component(component_file):
    character_strokes_nums = dict()
    component_set = set()
    file_object = open(component_file, 'r', encoding='UTF-8')
    for line in file_object:
        t = line.split(',')
        character = t[0]
        stroke_nums = t[1]
        component = t[2]
        character_strokes_nums[character] = stroke_nums
        for every_component in component:
            component_set.add(every_component)
    file_object.close()
    return character_strokes_nums, component_set


def update_component_dict(component_file, update_component_file):
    component_file_object = open(component_file, 'r', encoding='UTF-8')
    unkown_strokes = set()
    update_componet_file_object = open(update_component_file, 'w', encoding='UTF-8')
    # 存储汉字的笔划数量信息
    character_strokes_num = dict()
    # 存储汉字的组成部分信息
    character_component = dict()
    # 未知组成部分的汉字，转为存储首尾组成部分信息
    unkown_character_component = dict()
    for line in component_file_object:
        t = line.split('\t')
        character = t[0]
        comp_beg_end = t[1].split(',')[2]
        stroke_nums = len(t[1].split(',')[1])
        component = t[1].split(',')[3]
        character_strokes_num[character] = stroke_nums
        if component == "无汉字部件构造":
            unkown_character_component[character] = comp_beg_end
        else:
            character_component[character] = component
    print(f"已知汉字组件的汉字数量：{len(character_component)}")
    print(f"未知汉字组件的汉字数量：{len(unkown_character_component)}")
    update_character_count = 0
    for chara in unkown_character_component.keys():
        beg_end = unkown_character_component[chara]
        for com in beg_end:
            if com in character_component.keys():
                update_character_count += 1
                beg_end.replace(com, character_component[com])
        character_component[chara] = beg_end
    print(f"更新未知组件的组件数量：{update_character_count}")
    print(f"更新后已知汉字组件的汉字数量：{len(character_component)}")
    for chara in character_component.keys():
        update_componet_file_object.write(chara+"\t")
        components = character_component[chara]
        update_componet_file_object.write(str(character_strokes_num[chara])+"\t")
        for com in components:
            if com in character_strokes_num.keys():
                update_componet_file_object.write(com + ":" + str(character_strokes_num[com])+",")
            else:
                unkown_strokes.add(com)
                update_componet_file_object.write(com + ":0,")
        update_componet_file_object.write('\n')
    component_file_object.close()
    update_componet_file_object.close()
    print(unkown_strokes)
    print(len(unkown_strokes))
    # 已知汉字组件的汉字数量：8068
    # 未知汉字组件的汉字数量：12826
    # 更新未知组件的组件数量：23728
    # 更新后已知汉字组件的汉字数量：20894


def load_word_vector(Word_Vector_file, words):
    # 加载词向量,返回字典
    Word_Vector_dict = dict()
    word_vector_file_object = open(Word_Vector_file, 'r', encoding='UTF-8')
    # 立个flag 用来区别第一行
    flag = 0
    vector_size = 0
    for line in word_vector_file_object:
        t = line.strip('\n').split(' ')
        if flag == 0:
            words_nums = t[0]
            vector_size = int(t[1])
            print(f"总计有{words_nums}个词")
            print(f"未更新词的向量维度：{vector_size}")
            flag = 1
            continue
        if t[0] in words:
            Word_Vector_dict[t[0]] = np.array(list(map(lambda x: float(x), t[1:vector_size + 1])))
    print(f"加载到词向量：{len(Word_Vector_dict)}个")
    word_vector_file_object.close()
    return Word_Vector_dict


def load_component_vector(component_vector_file):
    # 参数: 组件向量文件路径
    component_vector_object = open(component_vector_file, 'r', encoding='UTF-8')
    Component_Vector_dict = dict()
    flag = 0
    size = 0
    for line in component_vector_object:
        ll = line.strip("\n").split(" ")
        if flag == 0:
            flag = 1
            # 词数
            word_nums = line.split(' ')[0]
            print(f'组件总数量:{word_nums}')
            # 维度
            size = int(line.split(" ")[1])
            print(f"偏旁部首组件向量维度:{size}")
        else:
            character = ll[0]
            vector = ll[1:size+1]
            Component_Vector_dict[character] = np.array(list(map(lambda x: float(x), vector)))
    component_vector_object.close()
    print(f"获取部件向量总数:{len(Component_Vector_dict)}")
    return Component_Vector_dict, size


def Component2Character(component_vector, Components_weight_dict, words, vector_size):
    # 将组件向量加和成汉字向量，不需要取平均
    Character_vector_dict = dict()
    character_set = set()
    for word in words:
        for chara in word:
            character_set.add(chara)
    print(f"汉字数量:{len(character_set)}")
    for character in character_set:
        if character in Components_weight_dict.keys():
            character_vector = np.zeros(vector_size)
            components = Components_weight_dict[character]
            for comp in components:
                if comp[0] in component_vector:
                    character_vector += float(comp[1]) * component_vector[comp[0]]
            Character_vector_dict[character] = character_vector
    print(f"得到汉字向量{len(Character_vector_dict)}组")
    return Character_vector_dict


def Character2Words(Character_vector_dict, Word_Vector_dict, words):
    update_Word_vector_dict = dict()
    # 将得到的字向量与原来的词向量加和，并且取平均
    for word in words:
        if word in Word_Vector_dict.keys():
            update_wordVector = Word_Vector_dict[word]
            character_nums = 0
            for character in word:
                if character in Character_vector_dict.keys():
                    character_nums += 1
                    update_wordVector += Character_vector_dict[character]
            # 将向量进行平均#################
            update_Word_vector_dict[word] = update_wordVector
            ################################
    return update_Word_vector_dict


def Print_update_WordVector(update_wordvector_dict, outfile, vector_size):
    out_file_object = open(outfile, 'w', encoding='UTF-8')
    out_file_object.write(str(len(update_wordvector_dict))+" "+str(vector_size)+"\n")
    for word in update_wordvector_dict.keys():
        out_file_object.write(word + " ")
        for w in update_wordvector_dict[word]:
            out_file_object.write(str(round(w, 6)) + " ")
        out_file_object.write("\n")
    out_file_object.close()
    print("更新向量打印完成")


def computer_component_weight(update_component_file):
    # 返回汉字中每个组件所占权重比值的字典
    update_component_file_object = open(update_component_file, 'r', encoding='UTF-8')
    components_weight_dict = dict()
    for line in update_component_file_object:
        t = line.strip("\n").split("\t")
        character = t[0]
        sum_stroke = int(t[1])
        computer_stroke = 0
        components = t[2].split(",")[:-1]
        for comp in components:
            tt = comp.split(":")
            stroke_num = int(tt[1])
            if stroke_num == 0:
                components.remove(comp)
            computer_stroke += stroke_num
        components_weight_list = subModel_computer_component_weight(sum_stroke, computer_stroke, components)
        # [('厂', '0.2857142857142857'), ('龙', '0.7142857142857143')]
        components_weight_dict[character] = components_weight_list
    update_component_file_object.close()
    return components_weight_dict


def subModel_computer_component_weight(sum_stroke, computer_stroke, components):
    # 参数:实际笔划数，计算笔划数，汉字组成部分 返回：各部分所占百分比的元祖
    components_weight_list = []
    if computer_stroke >= sum_stroke:
        reality_stroke = computer_stroke
    else:
        reality_stroke = sum_stroke
    for comp in components:
        t = comp.split(":")
        comp_tuple = (t[0], str(int(t[1])/reality_stroke))
        components_weight_list.append(comp_tuple)
    return components_weight_list


def subModel_computer_component_weight_update(sum_stroke, computer_stroke, components):
    components_weight_list = []
    if computer_stroke >= sum_stroke:
        reality_stroke = computer_stroke
    else:
        reality_stroke = sum_stroke
    for comp in components:
        t = comp.split(":")
        if len(components) > 1:
            comp_tuple = (t[0], str((reality_stroke - int(t[1])) / (reality_stroke*(len(components)-1))))
            components_weight_list.append(comp_tuple)
        else:
            components_weight_list.append((t[0], 1.0))
    # print(components_weight_list)
    return components_weight_list


if __name__ == '__main__':
    component_file = "C:\\Users\\Jamming_Lab\\Desktop\\汉字部首\\component.txt"
    update_component_file = "C:\\Users\\Jamming_Lab\\Desktop\\汉字部首\\update_component.txt"
    Words_file = "F:\\迅雷下载\\Words.txt"
    component_vector_file = "F:\\迅雷下载\\simply_wiki_component_update_vector.txt"
    word_vector_file = "F:\\迅雷下载\\seg_word2vector.txt"
    outfile = "F:\\迅雷下载\\simply_wiki_baseOn_strokes_numbers_component_vector.txt"
    #######################################################
    # 更新汉字组件表, 仅仅启用一次即可
    # update_component_dict(component_file, update_component_file)
    ########################################################

    Words = ebc.load_Words(Words_file)
    # 得到每个组件在汉字中所占权重
    components_weight_dict = computer_component_weight(update_component_file)
    # 加载各个组件的向量
    component_vector_dict, size = load_component_vector(component_vector_file)
    # 加载指定词向量词典
    Word_Vector_Dict = load_word_vector(word_vector_file, Words)
    # 将组件向量按照笔划权重组成汉字向量
    character_vector_dict = Component2Character(component_vector_dict, components_weight_dict, Words, vector_size=size)
    # 得到新的词向量
    update_Word_vector_dict = Character2Words(character_vector_dict, Word_Vector_Dict, Words)
    # 将新向量打印输出
    Print_update_WordVector(update_Word_vector_dict, outfile, size)

