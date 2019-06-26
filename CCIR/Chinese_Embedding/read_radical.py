# -*- coding: UTF-8 -*-


def read_radical():
    # 加载radical表中 4000多汉字的组成结构信息
    radical_dict = {}
    file_object = open("C:\\Users\\Jamming_Lab\\Desktop\\汉字部首\\radical.txt", 'r', encoding='UTF-8')
    for line in file_object:
        t = line.strip('\n').split('\t')
        if t[0] not in radical_dict.keys():
            radical_dict[t[0]] = t[4][3:]
    file_object.close()
    print(f"加载部首数量:{len(radical_dict)}")
    return radical_dict


def read_chaizi(unkown_character_set):
    # 用户补充上一个字典中未查找到到的字，参数是：未找到字符集合
    # 加载拆字字典，并且返回拆字字典集合，其中key是汉字，value是汉字组成偏旁部首的集合
    file_object = open("C:\\Users\\Jamming_Lab\\Desktop\\汉字部首\\chaizi.txt", 'r', encoding='UTF-8')
    extend_character_dict = {}
    for line in file_object:
        t = line.strip('\n').split("\t")
        if t[0] in unkown_character_set:
            if len(t) > 2:
                extend_character_dict[t[0]] = t[2]
            else:
                extend_character_dict[t[0]] = t[1]
    file_object.close()
    return extend_character_dict


def read_wiki():
    # 加载语料库，并且得到汉字字符集合
    file_object = open("F:\\迅雷下载\\simply_wiki.zh.text", 'r', encoding='UTF-8')
    Character_set = set()
    print("开始加载语料库")
    for line in file_object:
        line = line.replace(" ", "").strip("\n")
        for chara in line:
            Character_set.add(chara)
    file_object.close()
    print(f"汉字总数:{len(Character_set)}")
    # print(Character_set)
    return Character_set


def writer_all_component():
    out_file_object = open("C:\\Users\\Jamming_Lab\\Desktop\\汉字部首\\汉字组件表.txt", 'w', encoding="UTF-8")
    Character_set = read_wiki()
    radical_dict = read_radical()
    unknown_character_set = list(Character_set.difference(set(radical_dict.keys())))
    print(f"未找到部首的汉字数量:{len(unknown_character_set)}")
    extend_character_dict = read_chaizi(unknown_character_set)
    print(f"补足汉字部首数量:{len(extend_character_dict)}")
    no_find_character_set = list(set(unknown_character_set).difference(set(extend_character_dict.keys())))
    print(no_find_character_set)
    for ch in radical_dict.keys():
        out_file_object.write(ch+"\t"+radical_dict[ch]+"\n")
    for exch in extend_character_dict.keys():
        out_file_object.write(exch+"\t"+extend_character_dict[exch]+"\n")
    out_file_object.close()


def read_all_component():
    # 加载汉字偏旁部首表
    component_set = set()
    file_object = open("C:\\Users\\Jamming_Lab\\Desktop\\汉字部首\\汉字组件表.txt", 'r', encoding='UTF-8')
    for line in file_object:
        t = line.strip('\n').split('\t')
        for c in t[1]:
            component_set.add(c)
    file_object.close()
    print(component_set)
    print(f"总计component数量:{len(component_set)}")


if __name__ == '__main__':
    read_all_component()

