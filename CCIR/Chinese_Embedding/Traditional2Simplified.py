# -*- coding: utf-8 -*-
from langconv import *


def Traditional2Simplified(sentence):
    '''
    将sentence中的繁体字转为简体字
    :param sentence: 待转换的句子
    :return: 将句子中繁体字转换为简体字之后的句子
    '''
    sentence = Converter('zh-hans').convert(sentence)
    return sentence


def Simplified2Traditional(sentence):
    '''
    将sentence中的简体字转为繁体字
    :param sentence: 待转换的句子
    :return: 将句子中简体字转换为繁体字之后的句子
    '''
    sentence = Converter('zh-hant').convert(sentence)
    return sentence


if __name__ == "__main__":
    # wiki_path = "F:\\迅雷下载\\Ansj_Segment_simply_wiki.zh.text"
    # simply_wiki_path = "F:\\迅雷下载\\Ansj_Segment_wiki.zh.text"
    wiki_path = "F:\\迅雷下载\\Words.txt"
    simply_wiki_path = "F:\\迅雷下载\\繁体_Words.txt"
    file_object = open(wiki_path, 'r', encoding="UTF-8")
    simply_wiki_object = open(simply_wiki_path, 'w', encoding='UTF-8')
    for line in file_object:
        # simplified_sentence = Traditional2Simplified(line)
        # simply_wiki_object.write(simplified_sentence)
        traditional_sentence = Simplified2Traditional(line)
        simply_wiki_object.write(traditional_sentence)
    file_object.close()
    simply_wiki_object.close()
    print("简繁体转换完成")

