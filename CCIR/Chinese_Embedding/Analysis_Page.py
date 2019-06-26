# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
import re
import os


def analysis_Single_page(Single_file_path):
    path = Single_file_path
    with open(path, 'r', encoding='UTF-8') as f_html:
        Soup = BeautifulSoup(f_html.read(), 'lxml')
        div = Soup.findAll(id="div_a1")
        match_begin_end_compoment = re.search(r'首尾分解查字</span> ]：(.*?).\n', str(div), re.M | re.I)
        match_component = re.search(r'汉字部件构造</span> ]：(.*?).\n', str(div), re.M | re.I)
        match_stroke_number = re.search(r'笔顺编号</span> ]：(.*?)<br/>', str(div), re.M | re.I)
        match_stroke_order = re.search(r'笔顺读写</span> ]：(.*?)<br/>', str(div), re.M | re.I)

        if match_stroke_order:
            stroke_order = match_stroke_order.group(1)
        else:
            stroke_order = "无笔顺读写"

        if match_stroke_number:
            stroke_number = match_stroke_number.group(1)
        else:
            stroke_number = "无笔顺编号"

        if match_begin_end_compoment:
            begin_end_compoment = match_begin_end_compoment.group(1).split("(")[0]
        else:
            begin_end_compoment = "无首尾分解字"

        if match_component:
            component = match_component.group(0).split("：")[1].strip('\n')
        else:
            component = "无汉字部件构造"

        # print(f"笔顺读写:{stroke_order}")
        # print(f"笔顺编号:{stroke_number}")
        # print(f"汉字首尾分解:{begin_end_compoment}")
        # print("汉字部件构造:{component}")
        return stroke_order, stroke_number, begin_end_compoment, component


def load_all_page(main_Floder):
    files = os.listdir(main_Floder)
    component_dict = dict()
    for file in files:
        character = file[0]
        Single_file = os.path.join(main_Floder, file)
        stroke_order, stroke_number, begin_end_compoment, component = analysis_Single_page(Single_file)
        component_dict[character] = [stroke_order, stroke_number, begin_end_compoment, component]
    return component_dict


def Writer_component_file(component_dict, component_file):
    component_file_object = open(component_file, 'w', encoding='UTF-8')
    for ch in component_dict.keys():
        component_file_object.write(ch + "\t")
        for elem in component_dict[ch]:
            component_file_object.write(elem + ",")
        component_file_object.write("\n")
    component_file_object.close()


if __name__ == '__main__':
    main_Floder = "C:\\Users\\Jamming_Lab\\Desktop\\汉字部首\\hanzi"
    component_file = "C:\\Users\\Jamming_Lab\\Desktop\\汉字部首\\component.txt"
    component_dict = load_all_page(main_Floder)
    Writer_component_file(component_dict, component_file)
    print("解析成功")
