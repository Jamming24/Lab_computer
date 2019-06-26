# -*- coding: UTF-8 -*-
# 将汉字拆分成偏旁部首制作训练语料


def read_all_component():
    component_dict = {}
    file_object = open("C:\\Users\\Jamming_Lab\\Desktop\\汉字部首\\汉字组件表.txt", 'r', encoding='UTF-8')
    for line in file_object:
        t = line.strip('\n').split('\t')
        component_dict[t[0]] = t[1]
    file_object.close()
    print(f"加载部首数量:{len(component_dict)}")
    return component_dict


def read_all_component_update():
    component_dict = {}
    file_object = open("C:\\Users\\Jamming_Lab\\Desktop\\汉字部首\\update_component.txt", 'r', encoding='UTF-8')
    for line in file_object:
        t = line.strip('\n').split('\t')
        components = t[2].split(',')
        components_string = ""
        for com in components:
            if len(com.split(":")) > 1:
                components_string += com.split(":")[0]
        component_dict[t[0]] = components_string
    file_object.close()
    print(f"加载部首数量:{len(component_dict)}")
    return component_dict


def create_component_corpus(component_dict):
    print("开始加载语料库")
    file_object = open("F:\\迅雷下载\\simply_wiki.zh.text", 'r', encoding='UTF-8')
    out_file_object = open("F:\\迅雷下载\\simply_wiki_component_corpus.text", 'w', encoding='UTF-8')
    unkonw_traditional_character = set()
    traditional_character = set()
    for line in file_object:
        line = line.replace(" ", "").strip("\n")
        newLine = ""
        for chara in line:
            if chara in component_dict.keys():
                traditional_character.add(chara)
                for component in component_dict[chara]:
                    newLine += component+" "
            else:
                unkonw_traditional_character.add(chara)
        out_file_object.write(newLine+"\n")
        del newLine
    file_object.close()
    out_file_object.close()
    print(f"未匹配到汉字数量:{len(unkonw_traditional_character)}")
    # 未匹配到汉字数量:8497
    print(f"匹配到汉字数量{len(traditional_character)}")
    # 匹配到汉字数量17353
    print("语料构建完成")


if __name__ == '__main__':
    component_dict = read_all_component()
    # component_dict = read_all_component_update()
    create_component_corpus(component_dict)

