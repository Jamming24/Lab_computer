# -*- coding: UTF-8 -*-

# 加载CCMT评测数据集

root = "D:\\CCMT\\CCMT评测数据\\1.汉英新闻领域机器翻译-CCMT2019-CE-HLJIT"


def load_xml(test_path):
    count = 0
    file_open = open(test_path, 'r', encoding='UTF-8')
    test_data_set = []
    for line in file_open:
        if count > 3 and len(line) > 10:
            begin_local = line.index(">")
            end_local = line.index("</seg>")
            line = line[begin_local+1: end_local]
            test_data_set.append(line)
            print(line)
        else:
            count += 1
    file_open.close()
    return test_data_set


def print_test_file(out_path, test_data_set):
    file_open = open(out_path, 'w', encoding='UTF-=8')
    for line in test_data_set:
        file_open.write(line+"\n")
    file_open.close()


if __name__ == '__main__':
    test_path = root +"\\dev2019\\CWMT2018-WMT2018-TestSet-CE\\CWMT2018-TestSet-CE\\CWMT2018_CE_News_Test_src_2481.zh-src.xml"
    out_path = root+"\\dev2019\\CWMT2018-WMT2018-TestSet-CE\\CWMT2018-TestSet-CE\\CWMT2018_CE_News_Test_src_2481.zh-src.txt"

    test_path = root + "\\dev2019\\CWMT2018-WMT2018-TestSet-CE\\CWMT2018-TestSet-CE\\CWMT2018_CE_News_Test_tgt_2481.en-ref.xml"
    out_path = root + "\\dev2019\\CWMT2018-WMT2018-TestSet-CE\\CWMT2018-TestSet-CE\\CWMT2018_CE_News_Test_src_2481.en-ref.txt"

    test_data_set = load_xml(test_path)
    print_test_file(out_path, test_data_set)