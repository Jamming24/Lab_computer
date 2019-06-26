# -*- coding: utf-8 -*-

# import thulac
import jieba


# def thalac_segment_word():
#     # 清华分词
#     # thu1 = thulac.thulac(seg_only=True)
#     input_text = "F:\\迅雷下载\\wiki.zh.text"
#     output_text = "F:\\迅雷下载\\THU_Segment_wiki.zh.text"
#     # thu1.cut_f(input_text, output_text)
#     input_object = open(input_text, 'r', encoding="UTF-8")
#     output_object = open(output_text, 'w', encoding="UTF-8")
#     # 12:18
#     for line in input_object:
#         try:
#             t = thu1.cut(line.replace(" ", ""), text=True)
#         except IndexError:
#             print("出现异常行")
#             continue
#         output_object.write(t+"\n")
#     input_object.close()
#     output_object.close()
#     print("清华分词处理完成")


def jieba_segment_word():
    file_read = open(r"F:\\迅雷下载\\wiki.zh.text", "r", encoding="UTF-8")
    file_write = open(r"F:\\迅雷下载\\JieBa_Segment_wiki.zh.txt", "w", encoding="UTF-8")
    for sentence in file_read:
        new_sentence = sentence.replace(" ", "")
        cut = jieba.lcut(new_sentence, cut_all=False)
        sentence = " ".join(cut)
        # 这里得到的句子是把标点符号去掉，没有分词的句子
        file_write.write(sentence)
    file_read.close()
    file_write.close()
    print('jieba分词处理完成')


def jieba_segment_word(infile, outfile):
    file_read = open(infile, "r", encoding="UTF-8")
    file_write = open(outfile, "w", encoding="UTF-8")
    for sentence in file_read:
        new_sentence = sentence.replace(" ", "")
        cut = jieba.lcut(new_sentence, cut_all=False)
        sentence = " ".join(cut)
        # 这里得到的句子是把标点符号去掉，没有分词的句子
        file_write.write(sentence)
    file_read.close()
    file_write.close()
    print('jieba分词处理完成')

if __name__ == '__main__':
    # jieba_segment_word()
    infile = "D:\\CCMT\\CCMT评测数据\\1.汉英新闻领域机器翻译-CCMT2019-CE-HLJIT\\parallel\\_CCMT_ALL\\CCMT_src_train_ch_未分词.txt"
    outfile = "D:\\CCMT\\CCMT评测数据\\1.汉英新闻领域机器翻译-CCMT2019-CE-HLJIT\\parallel\\_CCMT_ALL\\CCMT_src_train_ch.txt"

    jieba_segment_word(infile, outfile)
    # thalac_segment_word()
