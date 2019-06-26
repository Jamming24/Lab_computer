# coding = utf-8

import os
import math

def readDataSet(FileFloder, OutFilePath):
    FileNames = os.listdir(FileFloder)
    Out_File = open(OutFilePath, 'w', encoding="UTF-8")
    for file in FileNames:
        simple_file_Path = os.path.join(FileFloder, file)
        print(simple_file_Path)
        file_object = open(simple_file_Path, 'r', encoding="UTF-8")
        file_data = file_object.readlines()
        for line in file_data:
            temp = line.split("\t")
            try:
                behavior_data = temp[2]
            except Exception:
                print("数组下标异常")
            else:
                behaviors = behavior_data.split(',')
                for be in behaviors:
                    everySimple = be.split("|")
                    try:
                        beginTime = everySimple[2]
                        endTime = everySimple[1]
                    except Exception:
                        print("数组下标越界")
                    else:
                        time = int(beginTime) - int(endTime)
                        if time < 0:
                            time = 0
                            time = 1/(1+1/(math.exp(time)))
                        else:
                            try:
                                time = 1/(1+1/(math.exp(time)))
                            except OverflowError:
                                time = float('inf')
                        Out_File.write(temp[0] + '\t' + everySimple[0] + '\t' + str(time) + '\t' + everySimple[1] + '\n')
        file_object.close()
        del temp
        del file_object
        del file_data
    Out_File.close()


FileFloder = "E:\\CCIR\\可计算数据\\Test_Set"
OutFilePath = "E:\CCIR\可计算数据\\behavior_formal.txt"
readDataSet(FileFloder, OutFilePath)
