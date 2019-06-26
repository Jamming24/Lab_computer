# coding=utf-8


def loadata(filePath, OutFile):
    temp_list = []
    train_line = ""
    file_object = open(filePath, 'r', encoding='UTF-8')
    Out_file_Path = open(OutFile, 'w', encoding='UTF-8')
    for line in file_object:
        t = line.split('\t')
        tt = t[2].split(',')
        # tt.remove("\n")
        for id in tt:
            train_line = train_line + id.split("|")[0] + " "
        if train_line != "":
            temp_list.append(train_line)
        train_line = ""
    for index in temp_list:
        Out_file_Path.write(index+"\n")
    Out_file_Path.close()


filePath = "E:\\CCIR\\available_new_testing_set.txt"
OutFile = "E:\\word2vector_testing_set.txt"
loadata(filePath, OutFile)
