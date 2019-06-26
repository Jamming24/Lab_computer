# encoding:utf-8
# CCIR线下评测评价程序升级版
import math


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
        for index in range(0, len(pp) - 1):
            pridect_list.append(pp[index])
        pridect_dict[test_ID[count]] = pridect_list
        count += 1
    right_count = 0
    for answer in test_ID:
        real_answer = answer_dict[answer]
        real_short_ID = real_answer[:4] + real_answer[28:32]
        pridect_answers = pridect_dict[answer]
        if real_short_ID in pridect_answers:
            local = pridect_answers.index(real_short_ID)
            temp_score = 1 / math.log10(local + 2)
            print(f"用户ID:{answer}, 真实答案ID:{real_short_ID}, 预测答案ID对应位置:{local+1}")
            right_count += 1
            total_score += (temp_score / denomit)
    answerfile_object.close()
    pridectfile_object.close()
    NDCG_Score = 10 * (total_score / len(answer_dict))
    print(f"test用户总量:{len(test_ID)}, 预测正确数量:{right_count}")
    return NDCG_Score


if __name__ == '__main__':
    #####################################################
    # 正确答案路径
    answerfile = "F:\\CCIR_eval\\CCIR_test_eval_answer.txt"
    # 预测答案路径
    pridectfile = "F:\\CCIR_eval\\test_combin_result.csv"
    NDCG_Score = Computer_NDCG(answerfile, pridectfile)
    print('NDCG得分:', NDCG_Score)
    ######################################################


