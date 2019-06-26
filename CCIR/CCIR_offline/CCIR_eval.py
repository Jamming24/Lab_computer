# encoding:utf-8
# CCIR线下评测评价程序
import math


def get_testing_set(purity_training_set, answer_id_dict, candidate_list, outfile, answer_outfile):
    test_list = dict()
    out_answer_list = dict()
    purity_file = open(purity_training_set, 'r', encoding='UTF-8')
    answer_outfile_object = open(answer_outfile, 'w', encoding='UTF-8')
    out_object = open(outfile, 'w', encoding='UTF-8')
    for line in purity_file:
        if len(test_list) == 135089:
            break
        else:
            tt = line.split('\t')
            answers_list = tt[2].strip('\n').split(",")
            # temp_set = set()
            # for ans in answers_list:
            #     ttt = ans.split("|")
            #     ansID = ttt[0]
            #     if ansID in temp_set:
            #         answers_list.remove(ans)
            #     else:
            #         temp_set.add(ansID)
            # temp_set.clear()
            if len(answers_list) > 3:
                last_answer = answers_list[len(answers_list)-4]
                parts = last_answer.split("|")
                if parts[0][0] == 'A':
                    longID = answer_id_dict[parts[0][1:len(parts[0])]]
                    if parts[2] != '0' and longID in candidate_list:
                        test_list[tt[0]] = answers_list[0:len(answers_list)-4]
                        out_answer_list[tt[0]] = last_answer+','+longID
    for key in test_list.keys():
        out_object.write(key + '\t\t')
        for li in test_list[key][0:len(test_list[key])-1]:
            out_object.write(li + ",")
        if len(test_list[key]) != 0:
            out_object.write(test_list[key][len(test_list[key])-1])
        out_object.write('\n')
    out_object.close()
    for ans in out_answer_list.keys():
        answer_outfile_object.write(ans + '\t')
        answer_outfile_object.write(out_answer_list[ans] + '\n')
    answer_outfile_object.close()


def load_answer_dict(answer_id_dict_file):
    answer_id_dict = dict()
    file_object = open(answer_id_dict_file, 'r', encoding='UTF-8')
    for line in file_object:
        answer_id_dict[line.split('\t')[0]] = line.split('\t')[1][:32]
    file_object.close()
    return answer_id_dict


def load_revers_answer_dict(answer_id_dict_file):
    # 根据长ID找短ID
    revers_answer_id_dict = dict()
    file_object = open(answer_id_dict_file, 'r', encoding='UTF-8')
    for line in file_object:
        revers_answer_id_dict[line.split('\t')[1][:32]] = line.split('\t')[0]
    return revers_answer_id_dict


def load_candidate(candidate_file):
    candidate_list = []
    file_object = open(candidate_file, 'r', encoding='UTF-8')
    for line in file_object:
        candidate_list.append(line.split('\t')[1][:32])
    print(len(candidate_list))
    return candidate_list


def Computer_NDCG(answerfile, pridectfile):
    total_score = 0.0
    test_ID = []
    denomit = 1
    count = 0
    answerfile_object = open(answerfile, 'r', encoding='UTF-8')
    pridectfile_object = open(pridectfile, 'r', encoding='UTF-8')
    answer_dict = dict()
    pridect_dict = dict()
    for answerline in answerfile_object:
        tt = answerline.split('\t')
        answer_dict[tt[0]] = tt[1].split(',')[1]
        test_ID.append(tt[0])
    for pridectline in pridectfile_object:
        pp = pridectline.strip('\n').split(',')
        pridect_list = []
        for index in range(0, len(pp)-1):
            pridect_list.append(pp[index])
        pridect_dict[test_ID[count]] = pridect_list
        count += 1
    for answer in answer_dict.keys():
        real_answer = answer_dict[answer]
        real_short_ID = real_answer[:4] + real_answer[28:32]
        pridect_answers = pridect_dict[answer]
        if real_short_ID in pridect_answers:
            local = pridect_answers.index(real_short_ID)
            temp_score = 1 / math.log10(local+2)

            total_score += (temp_score / denomit)
    answerfile_object.close()
    pridectfile_object.close()
    NDCG_Score = 10 * (total_score / len(answer_dict))
    return NDCG_Score


def get_training(eval_training_set, outfile):
    train_list = []
    purity_file = open(eval_training_set, 'r', encoding='UTF-8')
    test_outfile_object = open(outfile, 'w', encoding='UTF-8')
    for line in purity_file:
        if len(train_list) == 135089:
            for ln in train_list:
                test_outfile_object.write(ln)
            test_outfile_object.flush()
            train_list.clear()
            print("IO刷新一次")
        else:
            tt = line.split('\t')
            answers_list = tt[2].strip('\n').split(",")
            if len(answers_list) > 0:
                temp_set = set()
                temp_list = []
                answers_list.remove("")
                for answer in answers_list:
                    parts = answer.split("|")
                    if parts[0] in temp_set:
                        continue
                    else:
                        temp_set.add(parts[0])
                        temp_list.append(answer)
                temp_line = tt[0] + '\t' + str(len(temp_list)) + '\t'
                temp_set.clear()
                for ans in temp_list:
                    temp_line =temp_line + ans + ","
                train_list.append(temp_line+"\n")
            else:
                train_list.append(line)
    for ln in train_list:
        test_outfile_object.write(ln)
    test_outfile_object.close()
    print(len(train_list))
    train_list.clear()
    print("修复完成")

##########################################################


def loadTrainSet(train_file, answer_id_Dict):
    lineNum = 0
    Train_Set_dic = dict()
    file_object = open(train_file, 'r', encoding='UTF-8')
    for line in file_object:
        lineNum += 1
        if len(Train_Set_dic) == 135089:
            break
        temp = line.strip('\n').split('\t')
        if len(temp) == 8:
            User_ID = temp[0]
            answer_ID = temp[len(temp)-1]
            answer_time = temp[len(temp)-3]
            Behavior_list = temp[2].split(",")
            Behavior_list.append("A"+answer_id_Dict[answer_ID]+"|0"+"|"+answer_time[:10])
            if "" in Behavior_list:
                Behavior_list.remove("")
            if User_ID in Train_Set_dic.keys():
                temp_list = Train_Set_dic[User_ID]
                # temp_list.extend(Behavior_list)
                temp_list = list(set(temp_list).union(set(Behavior_list)))
                Train_Set_dic[User_ID] = temp_list
            else:
                Train_Set_dic[User_ID] = Behavior_list
    file_object.close()
    print("Train_Set_dic加载完成")
    return Train_Set_dic


def Print_addshowTest(Train_Set_dic, test2_file, outfile):
    out_file_object = open(outfile, 'w', encoding='UTF-8')
    test2_file_object = open(test2_file, 'r', encoding='UTF-8')
    test_ID = []
    for line in test2_file_object:
        tt = line.split('\t')
        test_ID.append(tt[0])
    print(f"testID大小:{len(test_ID)}")
    for userID in Train_Set_dic:
        if userID in test_ID:
            out_file_object.write(userID + '\t'+str(len(Train_Set_dic[userID])) + '\t')
            for answer in Train_Set_dic[userID]:
                out_file_object.write(answer+',')
        out_file_object.write('\n')
    test2_file_object.close()
    out_file_object.close()
    print("输出成功")


def Create_addshow_test(add_show_test_eval_file, outNewFile):
    file_object = open(add_show_test_eval_file, 'r', encoding='UTF-8')
    Out_file_object = open(outNewFile, 'w', encoding='UTF-8')
    for line in file_object:
        tt = line.strip('\n').split('\t')
        answers = tt[2].split(',')
        # print(tt[0],">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        if "" in answers:
            answers.remove("")
        temp_dict = dict()
        for ans in answers:
            temp_ans = ans.split('|')
            temp_dict[ans] = temp_ans[2]
        sort_truple = sorted(temp_dict.items(), key=lambda e: e[1], reverse=False)
        Out_file_object.write(tt[0] + '\t' + str(len(sort_truple)) + '\t')
        for items in sort_truple:
            # print(items[0], '>>>>', items[1])
            Out_file_object.write(items[0] + ',')
        Out_file_object.write('\n')
    file_object.close()
    Out_file_object
    print("输出完成")


if __name__ == '__main__':
    ###################################################
    candidate_file = "E:\\CCIR\\candidate.txt"
    answer_id_dict_file = "E:\\CCIR\\answer_id.dict"
    outfile = "F:\\CCIR_eval_with_show\\add_show_test_eval_3_3.txt"
    answer_outfile = "F:\\CCIR_eval_with_show\\add_show_test_eval_answer_3_3.txt"
    # purity_training_set = "E:\\purity_training_set.txt"
    infile = "F:\\CCIR_eval_with_show\\add_show_test_eval_3_2.txt"
    candidate_list = load_candidate(candidate_file)
    answer_id_dict = load_answer_dict(answer_id_dict_file)
    get_testing_set(infile, answer_id_dict, candidate_list, outfile, answer_outfile)
    #################################################################
    # file_object = open(answer_outfile, 'r', encoding='UTF-8')
    # ID_list = []
    # for line in file_object:
    #     tt = line.strip('\n').split('\t')
    #     ID_list.append(tt[0])
    # print(len(ID_list))
    # content_list = []
    # file_object_2 = open(infile, 'r', encoding='UTF-8')
    # for l in file_object_2:
    #     t = l.strip('\n').split('\t')
    #     if t[0] in ID_list:
    #         content_list.append(l)
    # out_object = open("F:\\out.txt", 'w', encoding='UTF-8')
    # for k in content_list:
    #     out_object.write(k)
    # file_object.close()
    # file_object_2.close()
    # out_object.close()
    #####################################################
    # 正确答案路径
    # answerfile = "F:\\CCIR_eval_with_show\\add_show_test_eval_answer_2.txt"
    # # # 预测答案路径
    # pridectfile = "F:\\CCIR_eval_with_show\\result_600_4_12.csv"
    # NDCG_Score = Computer_NDCG(answerfile, pridectfile)
    # print('NDCG得分:', NDCG_Score)
    ######################################################
    # file_object = open("F:\\CCIR_eval\\test_result.csv", 'r', encoding='UTF-8')
    # out_object = open("F:\\CCIR_eval\\out_result.csv", 'w', encoding='UTF-8')
    # for line in file_object:
    #     newLine = line.strip('\n')[:32]
    #     out_line = newLine[:4] + newLine[28:32]
    #     out_object.write(out_line+",\n")
    # out_object.close()
    # file_object.close()
    ######################################################
    # 修复训练数据bug
    # eval_training_set = "F:\\eval_training_set.txt"
    # outfile = "F:\\fix_eval_training_set_2.txt"
    # get_training(eval_training_set, outfile)
    ####################################################
    # 加载测试数据集合中展示但是用户未阅读的行为
    # train_file = "F:\\CCIR\\可计算数据\\competition\\training_set.txt"
    # answer_id_dict_file = "E:\\CCIR\\answer_id.dict"
    # test2_file = "F:\\CCIR_eval\\CCIR_test_eval_2.txt"
    # outfile = "F:\\add_show_test_eval_3.txt"
    # answer_id_Dict = load_revers_answer_dict(answer_id_dict_file)
    # Train_Set_dic = loadTrainSet(train_file, answer_id_Dict)
    # Print_addshowTest(Train_Set_dic, test2_file, outfile)
    #########################################################
    # add_show_test_eval_file = "F:\\CCIR_eval_with_show\\add_show_test_eval_3.txt"
    # outNewFile = "F:\\CCIR_eval_with_show\\add_show_test_eval_3_2.txt"
    # Create_addshow_test(add_show_test_eval_file, outNewFile)

