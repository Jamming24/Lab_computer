# encoding:utf-8
# 提取CCIR_test_eval 对应的查询词


def get_CCIR_test_eval(test_eval_file):
    # 获取每次用户行为的最后一个行为的行为发生时间，前提是展示时间为零
    testID = []
    file_object = open(test_eval_file, 'r', encoding='UTF-8')
    for line in file_object:
        tt = line.strip('\n').split('\t')
        testID.append(tt[0])
    file_object.close()
    print(f"testID大小 : {len(testID)}")
    return testID


def get_queryContent(training_file, testID):
    lineNum = 0
    query_Dict = dict()
    training_file_object = open(training_file, 'r', encoding='UTF-8')
    for line in training_file_object:
        lineNum += 1
        if lineNum == 600000:
            break
        tt = line.split('\t')
        if len(tt) > 5:
            userID = tt[0]
            # timeStamp = tt[5][:9]
            # if tt[1] == '0':
            #     if userID in testID_time.keys() and userID not in query_Dict.keys():
            #         query_Dict[userID] = tt[3]+"\t"+tt[4]
            #         # print(tt[3] + "\t" + tt[4])
            # else:
            #     if userID in testID_time.keys() and userID not in query_Dict.keys():
            #         answer_list = tt[2].split(',')
            #         time = answer_list[len(answer_list)-1].split("|")[2]
            #         if time == testID_time[userID]:
            #             query_Dict[userID] = tt[3]+"\t"+tt[4]
            #             # print(tt[3]+"\t"+tt[4])
            #         elif timeStamp == testID_time[userID]:
            #             query_Dict[userID] = tt[3] + "\t" + tt[4]
            if userID in testID:
                query_Dict[userID] = tt[3] + "\t" + tt[4]
    print(len(query_Dict))
    training_file_object.close()
    return query_Dict


def print_query_content(query_Dict, outfile):
    file_object = open(outfile, 'w', encoding='UTF-8')
    for key in query_Dict.keys():
        file_object.write(key+"\t")
        file_object.write(query_Dict[key]+"\n")
    file_object.close()


if __name__ == '__main__':
    test_eval_file = "F:\\CCIR_eval\\CCIR_test_eval.txt"
    training_file = "F:\\CCIR\\可计算数据\\competition\\training_set.txt"
    outfile = "F:\\CCIR_eval\\CCIR_test_query_content.txt"
    testID = get_CCIR_test_eval(test_eval_file)
    # query_Dict = get_queryContent(training_file, testID)
    # print_query_content(query_Dict, outfile)
    file_object = open(outfile, 'r', encoding='UTF-8')
    l = []
    for line in file_object:
        l.append(line.split('\t')[0])
    print(len(l))
    print(set(testID).difference(set(l)))
