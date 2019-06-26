# -*- coding:utf-8 -*-
'''
提取语料数据中所有的正例，即标签为1的样例
'''
from itertools import islice
def extract_p(data):
    # 一个小demo
    # result = data+'msrp_demo.txt'
    result = r'F:\tianliuyang\Developer\Gans\seqgan\data\quora_50K_train.txt'
    # result = r'F:\tianliuyang\Developer\Gans\seqgan\data\quora_50K_positive.txt'
    with open(result, 'w', encoding='utf-8', ) as epw:
        with open(data,'r',encoding='utf-8',) as ep:
            # 忽略第一行标签
            i = 0
            for x in islice(ep, 1,None):
                line = x.strip().split('\t')
                if line[5] == '1' and i < 50000:
                    # epw.write(line[3]+' '+line[4]+'\n')
                    epw.write(line[3]+'\n')
                else:
                    break
                i +=1

if __name__ == '__main__':
    # 一个小demo
    # data1 = r'F:\tianliuyang\Developer\Gans\seqgan\data\msrp_train.txt'
    data1 = r'F:\tianliuyang\Developer\Gans\seqgan\data\quora_150K.txt'
    extract_p(data1)

    # data2 = r'F:\tianliuyang\Developer\Gans\seqgan\data\msrp_test.txt'
    # extract_p(data2)

