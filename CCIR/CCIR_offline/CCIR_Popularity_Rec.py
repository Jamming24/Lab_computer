# encoding:utf-8
# 计算思想 筛选出与用户A相似度最高的n个用户，统计这n个用户阅读次数最多的k个答案
# 统计阅读次数，对阅读次数进行归一化处理，作为流行度分数，去流行度为前100的作为用户推荐列表
import os
import multiprocessing

def loadUserSimilarity(similarity_floder, k):
    # 每个用户取前k个最相关用户    k <= 100
    User_Similary_Dict = dict()
    filename_list = os.listdir(similarity_floder)
    for file in filename_list:
        all_lines = open(os.path.join(similarity_floder, file), 'r', encoding='UTF-8').readlines()
        for line in all_lines:
            user_list = []
            temp = line.split(":")
            UserID = temp[1][:32]
            if len(temp) >= k+2:
                n = k + 2
            else:
                n = len(temp)
            for i in range(2, n):
                user_list.append(temp[i][1:33])
            if len(user_list) != 0:
                User_Similary_Dict[UserID] = user_list
    return User_Similary_Dict


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
                if answer.split("|")[2] != '0':
                    answer_list.append(answer.split("|")[0])
        if len(answer_list) != 0:
            User_Behavior_Dict[userID] = answer_list
    print(f"test用户数量{len(User_Behavior_Dict)}")
    file_object.close()
    print(f"用户ID数量{len(test_ID)}")
    return User_Behavior_Dict, test_ID


def processManager(User_Behavior_Dict, User_Similary_dict, answer_id_dict_file, candidate_list, OutfileFloder):
    pool = multiprocessing.Pool(processes=6)
    User_Recommond_Dict = dict()
    count = 1
    result_list = []
    temp_User_Behavior_Dict = dict()
    for userID in User_Behavior_Dict.keys():
        if len(temp_User_Behavior_Dict) == 20000:
            Outfile = os.path.join(OutfileFloder, "Part_"+str(count)+".txt")
            count += 1
            part_User_Behavior_Dict = temp_User_Behavior_Dict.copy()
            temp_Item_Similary_dict = User_Similary_dict.copy()
            result = pool.apply_async(Computer_Popularity_degree,
                                      args=(part_User_Behavior_Dict, temp_Item_Similary_dict, answer_id_dict_file, candidate_list, Outfile))
            result_list.append(result)
            temp_User_Behavior_Dict.clear()
        else:
            temp_User_Behavior_Dict[userID] = User_Behavior_Dict[userID]

    last_part_User_Behavior_Dict = temp_User_Behavior_Dict.copy()
    last__Item_Similary_dict = User_Similary_dict.copy()
    Outfile = os.path.join(OutfileFloder, "Part_" + str(count) + ".txt")
    result = pool.apply_async(Computer_Popularity_degree,
                              args=(last_part_User_Behavior_Dict, last__Item_Similary_dict, answer_id_dict_file, candidate_list, Outfile))
    result_list.append(result)
    temp_User_Behavior_Dict.clear()
    pool.close()
    pool.join()

    for res in result_list:
        User_Recommond_Dict.update(res.get())
    print(f"总用户数量{len(User_Recommond_Dict)}")
    return User_Recommond_Dict


def Computer_Popularity_degree(User_Behavior_Dict, User_Similary_dict, answer_id_dict_file, candidate_list, Outfile):
    file_object = open(Outfile, 'w', encoding='UTF-8')
    name = multiprocessing.current_process().name
    print(f"进程{name}开始执行")
    answer_id_dict = load_answer_dict(answer_id_dict_file)
    User_Popularity_dict = dict()
    for userID in User_Behavior_Dict.keys():
        Simple_user_popular_dict = dict()
        if userID in User_Similary_dict.keys():
            related_user_list = User_Similary_dict[userID]
            item_list = User_Behavior_Dict[userID]
            for itemUser in related_user_list:
                if itemUser in User_Behavior_Dict.keys():
                    for relared_item in User_Behavior_Dict[itemUser]:
                        # 相关用户的所阅读过的文章ID
                        if relared_item in Simple_user_popular_dict.keys():
                            count = Simple_user_popular_dict[relared_item]
                            count += 1
                            Simple_user_popular_dict[relared_item] = count
                        else:
                            Simple_user_popular_dict[relared_item] = 1
            # print(f"》删除之前数量{len(Simple_user_popular_dict)}")
            for id in item_list:
                if id in Simple_user_popular_dict.keys():
                    del Simple_user_popular_dict[id]
            # print(f"》》删除之后数量{len(Simple_user_popular_dict)}")
            temp_dic = Simple_user_popular_dict.copy()
            for key in temp_dic.keys():
                if key not in candidate_list:
                    del Simple_user_popular_dict[key]
            del temp_dic
            # print(f"》》》候选推荐数量{len(Simple_user_popular_dict)}")

        if len(Simple_user_popular_dict) != 0:
            rec_list = []
            sort_popular_item = sorted(Simple_user_popular_dict.items(), key=lambda e: e[1], reverse=True)
            file_object.write(userID + "\t")
            for item in sort_popular_item:
                rec_list.append(answer_id_dict[item[0][1:len(item[0])]])
                file_object.write(item[0]+":"+str(item[1])+"\t")
            file_object.write("\n")
            User_Popularity_dict[userID] = rec_list
    print(f"推荐用户数量：{len(User_Popularity_dict)}")
    file_object.close()
    print(f"进程{name}计算结束")
    return User_Popularity_dict


def load_answer_dict(answer_id_dict_file):
    answer_id_dict = dict()
    file_object = open(answer_id_dict_file, 'r', encoding='UTF-8')
    for line in file_object:
        answer_id_dict[line.split('\t')[0]] = line.split('\t')[1][:32]
    file_object.close()
    return answer_id_dict


def load_resver_answer_dict(answer_id_dict_file):
    reverse_answer_id_dict = dict()
    file_object = open(answer_id_dict_file, 'r', encoding='UTF-8')
    for line in file_object:
        reverse_answer_id_dict[line.split('\t')[1][:32]] = line.split('\t')[0]
    file_object.close()
    return reverse_answer_id_dict


def load_candidate(candidate_file, answer_id_dict_file):
    reverse_answer_id_dict = load_resver_answer_dict(answer_id_dict_file)
    candidate_list = []
    file_object = open(candidate_file, 'r', encoding='UTF-8')
    for line in file_object:
        candidate_list.append("A"+reverse_answer_id_dict[line.split('\t')[1][:32]])
    print(len(candidate_list))
    return candidate_list


def get_Commit_csv(test_ID, User_Recommond_Dict, csv_out_file, n):
    out_file_object = open(csv_out_file, 'w', encoding='UTF-8')
    for user in test_ID:
        if user in User_Recommond_Dict.keys():
            result_list = User_Recommond_Dict[user]
            for index in range(0, n):
                if index < len(result_list):
                    ansID = result_list[index]
                    commit_ID = ansID[:4] + ansID[len(ansID)-4:len(ansID)]
                    out_file_object.write(commit_ID + ",")
                else:
                    out_file_object.write("-1,")
        else:
            for i in range(0, n):
                if i == 99:
                    out_file_object.write("-1")
                else:
                    out_file_object.write("-1,")
        out_file_object.write("\n")
    out_file_object.close()


if __name__ == '__main__':
    small_test_file = "E:\\CCIR\\testing_set_135089.txt"
    similarity_floder = "E:\\CCIR\\Similarity_betweenUser_Floder_3"
    answer_id_dict_file = "E:\\CCIR\\answer_id.dict"
    candidate_file = "E:\\CCIR\\candidate.txt"
    Outfile = "E:\\CCIR\\CCIR_Popularity_User_RecScore"
    csv_out_file = "E:\\CCIR\\Popularity\\result.csv"
    candidate_list = load_candidate(candidate_file, answer_id_dict_file)
    User_Behavior_Dict, test_ID = load_small_test(small_test_file)
    User_Similary_Dict = loadUserSimilarity(similarity_floder, 40)
    User_Popularity_dict = processManager(User_Behavior_Dict, User_Similary_Dict, answer_id_dict_file, candidate_list, Outfile)
    get_Commit_csv(test_ID, User_Popularity_dict, csv_out_file, 100)