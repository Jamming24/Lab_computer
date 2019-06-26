# encoding:utf-8
# 最后删除  为用户推荐 用户缺没有阅读的文章


def load_small_testID(small_test_file):
    test_ID = []
    file_object = open(small_test_file, 'r', encoding='UTF-8')
    for line in file_object:
        temp = line.split("\t")
        test_ID.append(temp[0])
    file_object.close()
    print(f"用户ID数量{len(test_ID)}")
    return test_ID


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


if __name__ == '__main__':
    UserCF_csv = open("E:\\CCIR\\Combine_final\\UserCF_6.4result.csv", 'r', encoding='UTF-8')
    ItemCF_csv = open("E:\\CCIR\\Combine_final\\ItemCF_result_with_question.csv", 'r', encoding='UTF-8')
    baseOnQuestion_csv = open("E:\\CCIR\\Combine_final\\CCIR_baseOnQuestion_result.csv", 'w', encoding='UTF-8')
    small_test_file = "E:\\CCIR\\testing_set_135089.txt"
    test_ID = load_small_testID(small_test_file)
    ItemCF_dic = dict()
    index = 0
    for item in ItemCF_csv:
        tt = item.strip('\n').split(',')
        simply_item_dic = dict()
        max_score = len()
        for i in range(0, len(tt)-1):
            ItemCF_dic[test_ID[index]] = tt
        index += 1
    for key in ItemCF_dic.keys():
        # print(key)
        print(ItemCF_dic[key])

    UserCF_csv.close()
    ItemCF_csv.close()
    baseOnQuestion_csv.close()