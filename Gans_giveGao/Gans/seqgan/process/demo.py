
# data1 = r'F:\tianliuyang\Developer\Gans\seqgan\data\msrp_train.txt'
# data2 = r'F:\tianliuyang\Developer\Gans\seqgan\data\msrp_test.txt'
# with open(data1,'r') as fr:
#     with open(data2,'r') as frr:
#         for x, y in zip(fr,frr):
#             print(x.strip(),y.strip())
import numpy as np
sentences = np.array([])
labels = np.array([])
seq_length = 82
positive_file = '../save/positive.txt'  # 原始句对用于判别的正例文件
negitive_file = '../save/negitive.txt'   # 原始句子+生成的句子构成的反例文件

def load_train_data(positive_file, negative_file):
    # Load data
    positive_examples = []
    negative_examples = []
    with open(positive_file)as fin:
        for line in fin:
            print(line)
            line = line.strip()
            line = line.split()
            parse_line = [int(x) for x in line]
            # 上面两行可以使用map进行优化
            # parse_line = map(int,line.split())
            if len(parse_line) == seq_length:
                positive_examples.append(parse_line)
    with open(negative_file)as fin:
        for line in fin:
            line = line.strip()
            line = line.split()
            print('len(line):',len(line))
            parse_line = [int(x) for x in line]
            # 上面两行可以使用map进行优化
            # parse_line = map(int,line.split())
            if len(parse_line) == seq_length:
                negative_examples.append(parse_line)
    print('len(positive_examples):',len(positive_examples))
    print('len(negative_examples):',len(negative_examples))
    sentences = np.array(positive_examples + negative_examples)
    print(sentences)
    # Generate labels
    positive_labels = [[0, 1] for _ in positive_examples]
    negative_labels = [[1, 0] for _ in negative_examples]
    labels = np.concatenate([positive_labels, negative_labels], 0)

load_train_data(positive_file,negitive_file)
dict = {}
dict.keys()