# coding = utf-8

import os
import gc
import math

def getHighFrequencyUser():
    file_object = open("E:\\CCIR\\user_behavior_statistics_all_search.txt", 'r', encoding="UTF-8")
    cool_file_object = open("E:\\CCIR\\cool_user_behavior_statistics_all_search.txt", 'w', encoding="UTF-8")
    hot_file_object = open("E:\\CCIR\\hot_user_behavior_statistics_all_search.txt", 'w', encoding="UTF-8")
    all_Content = file_object.readlines()
    for line in all_Content:
        temp = line.split(",")
        if int(temp[1]) < 20:
            cool_file_object.write(line)
            print(line)
        else:
            hot_file_object.write(line)

    file_object.close()
    cool_file_object.close()
    hot_file_object.close()


# noinspection PyBroadException
def statiscsTest():
    file_object = open("F:\\CCIR\\可计算数据\\competition\\testing_set.txt", 'r', encoding="UTF-8")
    User_file_object = open("E:\\CCIR\\user_infos.txt", 'r', encoding="UTF-8")

    test_hot_user_ID = open("E:\CCIR\\test_hot_user_ID.txt", 'w', encoding="UTF-8")
    test_cool_user_ID = open("E:\CCIR\\test_cool_user_ID.txt", 'w', encoding="UTF-8")
    test_hot_user = open("E:\CCIR\\test_hot_user.txt", 'w', encoding="UTF-8")
    test_cool_user = open("E:\CCIR\\test_cool_user.txt", 'w', encoding="UTF-8")

    allcount = 0
    user_behavior_dic = dict()
    all_user = User_file_object.readlines()

    data = file_object.readlines()
    for line in data:
        allcount += 1
        temp = line.split()
        try:
            id = temp[0]
        except Exception:
            print("发生数组下标越界")
            continue
        else:
            if id in user_behavior_dic.keys():
                value = user_behavior_dic[temp[0]]
                value += 1
                user_behavior_dic[temp[0]] = value
            else:
                user_behavior_dic[temp[0]] = 1


    for line in all_user:
        # print(line)
        temp = line.split("\t")
        try:
            topic_num = int(temp[5])
        except Exception:
            print("文本行异常，应予以跳过")
        else:
            if temp[0] in user_behavior_dic.keys():
                if topic_num > 3 and int(user_behavior_dic[temp[0]]) > 20:
                    test_hot_user_ID.write(temp[0] + "\n")
                    test_hot_user.write(line)
                else:
                    test_cool_user_ID.write(temp[0] + "\n")
                    test_cool_user.write(line)

    User_file_object.close()
    test_hot_user_ID.close()
    test_cool_user_ID.close()
    test_hot_user.close()
    test_cool_user.close()
    file_object.close()



def statisticsTrain():
    # 统计用户行为信息：统计每个用户用于多少条行为信息，对高频用户进行筛选，顺便将冷启动用户进行筛选
    # 且样本中行为数（交互 + 搜索词）小于 20 的样本」为冷启动用户样本

    # 代码逻辑  将每个文件读取到内存中,按照用户ID为key,用户行为数量为value

    testfloder = "E:\\CCIR测试数据"
    outfile = "E:\\CCIR测试数据\\user_behavior_statistics.txt"
    Files = os.listdir(testfloder)
    user_behavior_dic = dict()
    allcount = 0
    dicount = 0

    for file in Files:
        if len(file) > 18:
            simple_file_path = os.path.join(testfloder, file)
            file_object = open(simple_file_path, 'r', encoding='UTF-8')
            data = file_object.readlines()
            for line in data:
                allcount += 1
                temp = line.split()
                try:
                    id = temp[0]
                except Exception:
                    print("发生数组下标越界")
                    continue
                else:
                    if id in user_behavior_dic.keys():
                        value = user_behavior_dic[temp[0]]
                        value += 1
                        user_behavior_dic[temp[0]] = value
                    else:
                        user_behavior_dic[temp[0]] = 1


            file_object.close()
        else:
            continue
    # print(user_behavior_dic)
    print(f"数据行：{allcount}")

    out_file_object = open(outfile, 'w', encoding='UTF-8')
    for key in user_behavior_dic.keys():
        out_file_object.write(key + "," + str(user_behavior_dic[key]) + "\n")
        dicount += user_behavior_dic[key]
    out_file_object.close()

    print(f"总计：{dicount}行")


def splitfile():
    # 讲数据切割成100份
    path = "F:\\CCIR\\可计算数据\\competition\\training_set.txt"
    testpath = "F:\\CCIR\\可计算数据\\competition\\测试样本.txt"
    OutFolder = "E:\\CCIR\\中间数据\\"
    templist = list()
    file_object = open(path, 'r', encoding='UTF-8')
    line = file_object.readline()
    count = 0
    part = 1
    while line:
        # print(line)
        if count == 270000:
            Outfile_object = open(OutFolder + "training_set_Part" + str(part) + ".txt", 'w', encoding='utf-8')
            Outfile_object.writelines(templist)
            Outfile_object.close()
            print("training_set_Part" + str(part) + ".txt写入完成")
            part += 1
            count = 0
            del templist
            gc.collect()
            templist = list()
            templist.append(line)
        else:
            templist.append(line)
        count += 1
        line = file_object.readline()

    Outfile_object = open(OutFolder + "training_set_Part" + str(part) + ".txt", 'w')
    Outfile_object.writelines(templist)
    Outfile_object.close()
    templist.clear()
    print(count)


# splitfile()
# statisticsTrain()
# getHighFrequencyUser()

def processErrorline():
    file = "F:\\CCIR\\可计算数据\\competition\\answer_infos.txt"
    new_file = "E:\\CCIR\\available_answer_infos.txt"
    file_object = open(file, 'r', encoding='UTF-8')
    Out_file_object = open(new_file, 'w', encoding='UTF-8')
    count = 0
    text_list = []
    for line in file_object:
        count += 1
        if len(line.split('\t')[0]) != 32:
            temp_line = text_list[len(text_list)-1].strip("\n")
            text_list.pop()
            temp_line += line.strip("\n")
            text_list.append(temp_line+"\n")
        else:
            text_list.append(line)
    file_object.close()
    for li in text_list:
        Out_file_object.write(li)
    Out_file_object.close()


def load_answer_dict(answer_id_dict_file):
    answer_id_dict = dict()
    file_object = open(answer_id_dict_file, 'r', encoding='UTF-8')
    for line in file_object:
        answer_id_dict[line.split('\t')[0]] = line.split('\t')[1][:32]
    file_object.close()
    return answer_id_dict


def getUserReadAnswer():
    answer_id_dict_file = "E:\\CCIR\\answer_id.dict"
    available_file = "E:\\CCIR\\available_answer_infos.txt"
    out_file = "E:\\CCIR\\answer_map_topic.txt"
    shortId_file = open("E:\\无标题-2.txt", 'r', encoding='UTF-8')
    file_object = open(available_file, 'r', encoding='UTF-8')
    answer_id_dict = load_answer_dict(answer_id_dict_file)
    longId = []
    for id in shortId_file:
        if id[0] == 'A':
            longId.append(answer_id_dict[id.strip('\n')[1:len(id)]])
    print(f">>>>>>>{len(longId)}")
    answer_topic_dict = dict()
    for info in file_object:
        tt = info.split('\t')
        if len(tt[0]) == 32:
            topics = tt[len(tt)-1].strip('\n').split(',')
            if len(topics) != 0:
                answer_topic_dict[tt[0]] = topics
    print(f"answer_topic_dict:{len(answer_topic_dict)}")
    Out_file_object = open(out_file, 'w', encoding='UTF-8')
    for id in longId:
        if id in answer_topic_dict.keys():
            Out_file_object.write(id+"\t")
            for index in range(0, len(answer_topic_dict[id])-1):
                Out_file_object.write(answer_topic_dict[id][index] + ",")
            Out_file_object.write(answer_topic_dict[id][len(answer_topic_dict[id])-1][:32])
        Out_file_object.write('\n')
    Out_file_object.close()
    shortId_file.close()
    file_object.close()


def getUserReadQuestion():
    answer_id_dict_file = "E:\\CCIR\\answer_id.dict"
    available_file = "E:\\CCIR\\available_answer_infos.txt"
    out_file = "E:\\CCIR\\answer_map_question.txt"
    shortId_file = open("E:\\无标题-2.txt", 'r', encoding='UTF-8')
    file_object = open(available_file, 'r', encoding='UTF-8')
    answer_id_dict = load_answer_dict(answer_id_dict_file)
    longId = []
    for id in shortId_file:
        if id[0] == 'A':
            longId.append(answer_id_dict[id.strip('\n')[1:len(id)]])
    print(f">>>>>>>{len(longId)}")
    answer_question_dict = dict()
    for info in file_object:
        tt = info.split('\t')
        if len(tt[0]) == 32 and len(tt) > 1:
            question = tt[1]
            answer_question_dict[tt[0]] = question
    print(f"answer_question_dict:{len(answer_question_dict)}")
    Out_file_object = open(out_file, 'w', encoding='UTF-8')
    for id in longId:
        if id in answer_question_dict.keys():
            Out_file_object.write(id+"\t")
            Out_file_object.write(answer_question_dict[id])
        Out_file_object.write('\n')
    Out_file_object.close()
    shortId_file.close()
    file_object.close()


if __name__ == '__main__':
    # getUserReadAnswer()
    # getUserReadQuestion()
    a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    newA = []
    num = 1.0
    temp = []
    for key in a:
        newA.append([key, num])
        num += 1.0
    print(newA)
    for k in newA:
        temp.append(k[0])
    print(temp)
    temp.remove('b')
    for kk in a:
        if kk in temp:
            continue
        else:
            newA.append([kk, num])
            num += 1.0
    print(newA)








































