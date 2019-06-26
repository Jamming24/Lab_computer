# encoding:utf-8

# 加载smalltest 筛选出符合条件的 讲行为记录存到字典，然后 在到train中找到对应的ID 的
# 行为记录 然后再次筛选，得到符合条件的用户ID和行为记录，
# 最后  到small test中 找到对应的用户信息行，导出


def load_focusOnlessThressUserID(focusOnlessThressUserIDfile):
    # 加载用户关注数量少于3的用户ID
    focusOnlessThressUserID_list = []
    file_object = open(focusOnlessThressUserIDfile, 'r', encoding='UTF-8')
    for line in file_object:
        focusOnlessThressUserID_list.append(line[:32])
    return focusOnlessThressUserID_list


def get_Small_test_CoolUserID(small_test_file, focusOnlessThressUserID_list, train_Query_Behavior_less_20, test_CoolUserID_file):
    # 且样本中行为数（交互 + 搜索词）小于 20 的样本」为冷启动用户样本
    # 返回真正满足要求的冷启动用户ID
    Cool_UserID_list = []
    small_test_file_dic = dict()
    file = open(small_test_file, 'r', encoding='UTF-8')
    Out_file = open(test_CoolUserID_file, 'w', encoding='UTF-8')
    for line in file:
        t = line.split('\t')
        user = t[0]
        benum = t[1]
        querynum = t[len(t)-2]
        allsum = int(benum)+int(querynum)
        small_test_file_dic[user] = line
        if user in train_Query_Behavior_less_20.keys():
            if (allsum + train_Query_Behavior_less_20[user]) < 20:
                Cool_UserID_list.append(user)
    print(f"行为查询数量之和小于20的用户数:{len(Cool_UserID_list)}")
    Cool_UserID_list = list(set(Cool_UserID_list).intersection(set(focusOnlessThressUserID_list)))
    print(f"冷启动用户数量：{len(Cool_UserID_list)}")
    for id in Cool_UserID_list:
        Out_file.write(id+":"+str(train_Query_Behavior_less_20[id])+"\n")
    print("Cool_UserID保存完成")
    return Cool_UserID_list, small_test_file_dic


def load_train_behavior_file(train_behavior_file):
    # 返回行为数（交互 + 搜索词）小于 20 的用户ID
    train_Query_Behavior_less_20 = dict()
    file_object = open(train_behavior_file, 'r', encoding='UTF-8')
    for line in file_object:
        t = line.split(":")
        userID = t[0]
        num = int(t[1])
        if num < 20:
            train_Query_Behavior_less_20[userID] = num
    return train_Query_Behavior_less_20


def get_TrainQueryAndBehaviorNum (train_file, out_file):

    train_behavior = dict()
    file_object = open(train_file, 'r', encoding='UTF-8')
    Out_file_object = open(out_file, 'w', encoding='UTF-8')
    for line in file_object:
        t = line.split("\t")
        user = t[0]
        benum = t[1]
        querynum = t[3]
        allsum = int(benum) + int(querynum)
        if user in train_behavior.keys():
            train_behavior[user] = train_behavior[user] + allsum
        else:
            train_behavior[user] = allsum
    print(f"train用户总数:{len(train_behavior)}")
    for key in train_behavior.keys():
        Out_file_object.write(key+":"+str(train_behavior[key])+"\n")


def get_CoolUserFile(Cool_UserID_list , small_test_dic, coolUser_Outfile):
    file_object = open(coolUser_Outfile, 'w', encoding='UTF-8')
    for id in Cool_UserID_list:
        file_object.write(small_test_dic[id])
    file_object.close()
    print(f"{coolUser_Outfile}输出完成")


def get_CoolUserInfos(coolUser_ID_file, user_info_file, coolUserinfo_file):
    coolUser_file_object = open(coolUser_ID_file, 'r', encoding='UTF-8')
    user_info_file_object = open(user_info_file, 'r', encoding='UTF-8')
    coolUserinfo_file_object = open(coolUserinfo_file, 'w', encoding='UTF-8')
    coolUser_ID_list = []
    user_info_list = []
    for line in coolUser_file_object:
        coolUser_ID_list.append(line.split(":")[0])
    print(f"冷启动用户数量{len(coolUser_ID_list)}")
    for userline in user_info_file_object:
        if userline.split('\t')[0] in coolUser_ID_list:
            user_info_list.append(userline)
    print(f"得到冷启动用户信息数量:{len(user_info_list)}")
    coolUser_file_object.close()
    user_info_file_object.close()
    for user in user_info_list:
        coolUserinfo_file_object.write(user)
    coolUserinfo_file_object.close()
    print("写出成功")


if __name__ == '__main__':
    # 执行第一部分
    train_behavior_file = "E:\\CCIR\\train_set_behavior.txt"
    train_file = "E:\\CCIR\\available_training_set.txt"
    # get_TrainQueryAndBehaviorNum(train_file, train_behavior_file)
    ###################################################
    # 执行第二部分
    focusOnlessThressUserIDfile = "E:\\CCIR\\focusOnlessThressUserID.txt"
    small_test_file = "E:\\CCIR\\small_testing_set.txt"
    test_CoolUserID_file = "E:\\CCIR\\coolUser_ID.txt"
    coolUser_Outfile = "E:\\CCIR\\small_test_cool_User.txt"
    # # 加载关注话题数量小于3的用户ID
    # focusOnlessThressUserID_list = load_focusOnlessThressUserID(focusOnlessThressUserIDfile)
    # # 加载train文件中 用户行为数量和查询词数量小于20的用户ID
    # train_Query_Behavior_less_20 = load_train_behavior_file(train_behavior_file)
    # # 返回用户冷启动ID 并输出到文件
    # Cool_UserID_list, small_test_file_dic = get_Small_test_CoolUserID(small_test_file, focusOnlessThressUserID_list, train_Query_Behavior_less_20, test_CoolUserID_file)
    # # 得到冷启动用户文件
    # get_CoolUserFile(Cool_UserID_list, small_test_file_dic, coolUser_Outfile)
    ######################################################
    # 第三部分
    user_info_file = "E:\\CCIR\\user_infos.txt"
    coolUserinfo_file = "E:\\CCIR\\small_test_coolUser_infos.txt"
    get_CoolUserInfos(test_CoolUserID_file, user_info_file, coolUserinfo_file)
    #########################################################






