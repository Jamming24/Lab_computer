# encoding:utf-8
# 本程序功能 对于完整的测试集合用户，判断用户行为属于哪个话题，然后为用户推荐话题相关的优质答案，
# 判断用户行为属于哪个问题，为用户推荐该问题的其他优质答案
import os
import math
import multiprocessing


def load_small_test(small_test_file):
    test_ID = []
    User_Behavior_Dict = dict()
    file_object = open(small_test_file, 'r', encoding='UTF-8')
    for line in file_object:
        temp = line.split("\t")
        userID = temp[0]
        test_ID.append(userID)
        answer_list = []
        for answer in temp[2].split(","):
            if len(answer) != 0:
                t = answer.split("|")
                start_time = t[1]
                end_time = t[2]
                if int(end_time) != 0:
                    time_difference = int(start_time) - int(end_time)
                    if time_difference > 0:
                        answer_list.append([t[0], 1.0])
                    else:
                        score = 1 / (1 + 1 / (math.exp(time_difference / 60)))
                        answer_list.append([t[0], round(score, 6)])
        if len(answer_list) != 0:
            User_Behavior_Dict[userID] = answer_list
    print(f"test用户数量{len(User_Behavior_Dict)}")
    file_object.close()
    print(f"用户ID数量{len(test_ID)}")
    return User_Behavior_Dict, test_ID


def load_answer_dict(answer_id_dict_file):
    answer_id_dict = dict()
    file_object = open(answer_id_dict_file, 'r', encoding='UTF-8')
    for line in file_object:
        answer_id_dict[line.split('\t')[0]] = line.split('\t')[1][:32]
    file_object.close()
    return answer_id_dict


def load_topic_inverse_answer(topic_inverse_answer_file):
    topic_inverse_answer_dic = dict()
    file_object = open(topic_inverse_answer_file)
    for line in file_object:
        tt = line.split('\t')
        topic_inverse_answer_dic[tt[0]] = tt[1].strip('\n').split(',')[:-1]
    file_object.close()
    return topic_inverse_answer_dic


def estimate_excellent_answer(candidate_answer_file):
    # key为文章ID，值为1的是优质答案 ，值为2的时候是优质+编辑推荐答案，值为0的时候是普通答案
    file_object = open(candidate_answer_file, 'r', encoding='UTF-8')
    candidate_answer_quality = dict()
    for line in file_object:
        tt = line.split('\t')
        # 是否是优质答案
        exe_flag = tt[4]
        # 是否被编辑推荐
        rec_flag = tt[5]
        value = int(exe_flag) + int(rec_flag)
        # 被感谢的次数
        thanks = int(tt[9])
        # 被赞同的次数
        agree = int(tt[10])
        # 被收藏的次数
        save = int(tt[12])
        # 被反对的次数
        disagree = int(tt[13])
        # 收到没有帮助的次数
        nohelp = int(tt[15])
        count = thanks + agree + save - disagree - nohelp
        score = 1 / (1 + 1 / (math.exp(count/1000)))
        # print(tt[0], ">>>>>", score)
        candidate_answer_quality[tt[0]] = value/2 + score
    file_object.close()
    print(f"答案数量{len(candidate_answer_quality)}")
    return candidate_answer_quality


def get_Commit_csv(test_ID, Commit_user_recommond_dict, csv_out_file, n):
    out_file_object = open(csv_out_file, 'w', encoding='UTF-8')
    for user in test_ID:
        if user in Commit_user_recommond_dict.keys():
            result_list = Commit_user_recommond_dict[user]
            for index in range(0, n):
                if index < len(result_list):
                    ansID = result_list[index]
                    commit_ID = ansID[:4] + ansID[len(ansID)-4:len(ansID)]
                    out_file_object.write(commit_ID + ",")
                else:
                    out_file_object.write("-1,")
        else:
            # print(user)
            for i in range(0, n):
                if i == 99:
                    out_file_object.write("-1")
                else:
                    out_file_object.write("-1,")
        out_file_object.write("\n")
    out_file_object.close()


def get_User_read_question(User_Behavior_Dict, answer_id_dict_file, answer_map_question_file):
    answer_id_dict = load_answer_dict(answer_id_dict_file)
    answer_map_question_file_object = open(answer_map_question_file, 'r', encoding='UTF-8')
    user_read_questions_dic = dict()
    answer_map_question_dic = dict()
    for line in answer_map_question_file_object:
        tt = line.split('\t')
        if len(tt[1]) > 30:
            answer_map_question_dic[tt[0]] = tt[1].strip('\n')
    answer_map_question_file_object.close()
    print(f"answer_map_question_dic数量大小:{len(answer_map_question_dic)}")
    for user in User_Behavior_Dict.keys():
        Simply_user_read_question_dic = dict()
        for item in User_Behavior_Dict[user]:
            shortId = item[0][1:len(item[0])]
            shortId_Score = item[1]
            if shortId in answer_id_dict.keys():
                LongID = answer_id_dict[shortId]
                if LongID in answer_map_question_dic.keys():
                    question = answer_map_question_dic[LongID]
                    if question in Simply_user_read_question_dic.keys():
                        question_score = Simply_user_read_question_dic[question]
                        question_score += shortId_Score
                        Simply_user_read_question_dic[question] = question_score
                    else:
                        Simply_user_read_question_dic[question] = shortId_Score
        user_read_questions_dic[user] = Simply_user_read_question_dic
    return user_read_questions_dic


def get_baseOn_question_RecList(User_Behavior_Dict, user_read_question_dic, question_inverse_answer_dic, candidate_answer_quality, recfile):
    name = multiprocessing.current_process().name
    print(f"进程{name}开始执行")
    rec_out_file = open(recfile, 'w', encoding='UTF-8')
    User_RecCommond_dic = dict()
    User_Read_Answer_list = []
    for user in User_Behavior_Dict.keys():
        Simply_User_RecCommond_dic = dict()
        # 获取用户阅读过问题的ID列表
        for userScore in User_Behavior_Dict[user]:
            User_Read_Answer_list.append(userScore[0])
        # 计算用户推荐列表
        if user in user_read_question_dic.keys():
            topics = user_read_question_dic[user]
            for topicID in topics.keys():
                topic_score = topics[topicID]
                if topicID in question_inverse_answer_dic.keys():
                    topic_map_answers = question_inverse_answer_dic[topicID]
                    for answer in topic_map_answers:
                        if answer in candidate_answer_quality.keys() and answer not in User_Read_Answer_list:
                            answer_score = candidate_answer_quality[answer]
                            final_score = topic_score * answer_score
                            if answer in Simply_User_RecCommond_dic.keys():
                                temp_score = Simply_User_RecCommond_dic[answer]
                                Simply_User_RecCommond_dic[answer] = temp_score + final_score
                            else:
                                Simply_User_RecCommond_dic[answer] = final_score
        User_Read_Answer_list.clear()
        if len(Simply_User_RecCommond_dic) > 0:
            Simply_User_RecCommond_tuple_list = sorted(Simply_User_RecCommond_dic.items(), key=lambda e: e[1], reverse=True)[:200]
            # print(Simply_User_RecCommond_tuple_list)
            User_RecCommond_dic[user] = Simply_User_RecCommond_tuple_list
    for user in User_RecCommond_dic.keys():
        rec_out_file.write(user+'\t')
        for item in User_RecCommond_dic[user]:
            rec_out_file.write(item[0] + ":" + str(item[1])+",")
        rec_out_file.write('\n')
    rec_out_file.close()
    print(f"进程{name}计算结束")
    return User_RecCommond_dic


def multiprocessing_manager(n, User_Behavior_Dict, user_read_topics_dic, topic_inverse_answer_dic, candidate_answer_quality, OutfileFloder):

    # n为进程池最大进程数量
    # k值表示为与用户喜欢的物品最相关的k个物品
    User_Recommond_Dict = dict()
    result_list = []
    count = 1
    pool = multiprocessing.Pool(processes=n)
    temp_User_Behavior_Dict = dict()
    for userID in User_Behavior_Dict.keys():
        if len(temp_User_Behavior_Dict) == 10000:
            recfile = os.path.join(OutfileFloder, "Part_" + str(count) + ".txt")
            count += 1
            part_User_Behavior_Dict = temp_User_Behavior_Dict.copy()
            result = pool.apply_async(get_baseOn_question_RecList,
                                      args=(part_User_Behavior_Dict, user_read_topics_dic, topic_inverse_answer_dic, candidate_answer_quality, recfile))
            result_list.append(result)
            temp_User_Behavior_Dict.clear()
        else:
            temp_User_Behavior_Dict[userID] = User_Behavior_Dict[userID]

    last_part_User_Behavior_Dict = temp_User_Behavior_Dict.copy()
    result = pool.apply_async(get_baseOn_question_RecList, args=(last_part_User_Behavior_Dict, user_read_topics_dic, topic_inverse_answer_dic, candidate_answer_quality, recfile))
    result_list.append(result)
    temp_User_Behavior_Dict.clear()
    pool.close()
    pool.join()
    for res in result_list:
        User_Recommond_Dict.update(res.get())

    Commit_user_recommond_dict = dict()
    for user in User_Recommond_Dict.keys():
        Simply_list = []
        # print(User_Recommond_Dict[user])
        for item in User_Recommond_Dict[user]:
            Simply_list.append(item[0])
        Commit_user_recommond_dict[user] = Simply_list
    print(f"总用户数量{len(User_Recommond_Dict)}")

    return Commit_user_recommond_dict


if __name__ == '__main__':
    answer_id_dict_file = "E:\\CCIR\\answer_id.dict"
    small_test_file = "E:\\CCIR\\testing_set_135089.txt"
    answer_map_topic_file = "E:\\CCIR\\answer_map_question.txt"
    question_inverse_answer_file = "E:\\CCIR\\real_cool_user\\question_inverse_answer.txt"
    candidate_answer_file = "E:\\CCIR\\real_cool_user\\candidate_answer.txt"
    csv_out_file = "E:\\CCIR\\CCIR_baseOnQuestion_result.csv"
    recfile = "E:\\CCIR\\CCIR_baseOnQuestion_RecScore"
    User_Behavior_Dict, test_ID = load_small_test(small_test_file)
    user_read_topics_dic = get_User_read_question(User_Behavior_Dict, answer_id_dict_file, answer_map_topic_file)
    topic_inverse_answer_dic = load_topic_inverse_answer(question_inverse_answer_file)
    candidate_answer_quality = estimate_excellent_answer(candidate_answer_file)
    User_RecCommond_dic = multiprocessing_manager(7, User_Behavior_Dict, user_read_topics_dic, topic_inverse_answer_dic, candidate_answer_quality, recfile)
    get_Commit_csv(test_ID, User_RecCommond_dic, csv_out_file, 100)
    print("计算完成")