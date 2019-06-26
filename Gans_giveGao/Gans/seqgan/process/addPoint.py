# -*- coding:utf-8 -*-
def addpoint(pathin, pathout):
    with open(pathin, 'r') as fin, open(pathout, 'w') as fout:
        for line in fin:
            line = line.replace('\n', '')
            if line.endswith('.'):
                fout.write(line+'\n')
            else:
                fout.write(line + '.\n')


if __name__ == '__main__':
    path1 = '../data/msrp_demo.txt'
    path2 = '../data/en_demo2.txt'
    addpoint(path1, path2)
