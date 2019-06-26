# for decimal import Decimal
def eval(pre, label):
    tn = 0.0
    tp = 0.0
    fp = 0.0
    fn = 0.0

    for i in range(len(label)):
        if pre[i] == '0' and label[i] == '0':
            tn = tn + 1

        if pre[i] == '1' and label[i] == '1':
            tp = tp + 1

        if pre[i] == '1' and label[i] == '0':
            fp = fp + 1

        if pre[i] == '0' and label[i] == '1':
            fn = fn + 1

    # print(str(tn) + "\t" + str(tp) + "\t" + str(fp) + "\t" + str(fn))
    acc = (tp + tn) / (tp + tn + fp + fn)
    # print('acc', acc)
    f1 = float(2 * tp / (2 * tp + fp + fn))
    recall = float(tp / (tp + fn))
    if tp + fp == 0:
        return str(0.0), str(recall), str(acc), str(f1)
    else:
        prep = tp / (tp + fp)
        return str(prep), str(recall), str(acc), str(f1)

def read(path_ol, path_ed, path_me, path_ro):
    labels = []
    s_ol = []
    s_ed = []
    s_me = []
    s_ro = []
    s_avg = []
    s_f = []
    with open(path_ol, 'r') as fol, open(path_ed, 'r') as fed, open(path_me, 'r') as fme, open(path_ro, 'r') as fro:
        for _ in fol:
            labels.append(_.replace('\n', '').split('\t')[0])
            s_ol.append(_.replace('\n', '').split('\t')[3])
        for _ in fed:
            s_ed.append(_.replace('\n', '').split('\t')[3])
        for _ in fme:
            s_me.append(_.replace('\n', '').split('\t')[3])
        for _ in fro:
            s_ro.append(_.replace('\n', '').split('\t')[3])
    for i in range(len(labels)):
        s_avg.append((float(s_ol[i]) + float(s_ed[i]) + float(s_me[i]) + float(s_ro[i])) / 4)
        v = (float(s_ol[i]) + float(s_ed[i])) / 2
        s = (float(s_me[i]) + float(s_ro[i])) / 2
        s_f.append(float((2 * s * v) / (s + v)))
    return labels, s_ol, s_ed, s_me, s_ro, s_avg, s_f

# 阈值遍历得到pre
def getpre(tro, lis):
    pre = []
    for x in lis:
        if float(x) < float(tro):
            pre.append('0')
        else:
            pre.append('1')
    return pre


if __name__ == '__main__':

    path_ol = r'H:\DataScore\overlap.txt'
    path_ed = r'H:\DataScore\editd.txt'
    path_me = r'H:\DataScore\meteor.txt'
    path_ro = r'H:\DataScore\rouge.txt'
    result_ol = r'H:\DataScore\result_ol.txt'
    result_ed = r'H:\DataScore\result_ed.txt'
    result_me = r'H:\DataScore\result_me.txt'
    result_ro = r'H:\DataScore\result_ro.txt'
    result_avg = r'H:\DataScore\result_avg.txt'
    result_f = r'H:\DataScore\result_f.txt'
    labels, s_ol, s_ed, s_me, s_ro, s_avg, s_f = read(path_ol, path_ed, path_me, path_ro)
    i = 0.01
    with open(result_ol, 'w') as fw_ol, open(result_ed, 'w') as fw_ed, open(result_me, 'w') as fw_me, open(result_ro,
                                                                                                           'w') as fw_ro, open(
        result_avg, 'w') as fw_avg, open(result_f, 'w') as fw_f:
        for _ in range(100):
            pre_ol = getpre(i, s_ol)
            # print(pre_ol)
            prep_ol, recall_ol, acc_ol, f1_ol = eval(pre_ol, labels)
            fw_ol.write(
                str(i) +' prep, recall, acc, f1:' + '\t' + prep_ol + '\t' + recall_ol + '\t' + acc_ol + '\t' + f1_ol + '\n')

            pre_ed = getpre(i, s_ed)
            prep_ed, recall_ed, acc_ed, f1_ed = eval(pre_ed, labels)
            fw_ed.write(
                str(i)+ 'prep, recall, acc, f1:' + '\t' + prep_ed + '\t' + recall_ed + '\t' + acc_ed + '\t' + f1_ed + '\n')

            pre_me = getpre(i, s_me)
            prep_me, recall_me, acc_me, f1_me = eval(pre_me, labels)
            fw_me.write(
                str(i)+'prep, recall, acc, f1:' + '\t' + prep_me + '\t' + recall_me + '\t' + acc_me + '\t' + f1_me + '\n')

            pre_ro = getpre(i, s_ro)
            prep_ro, recall_ro, acc_ro, f1_ro = eval(pre_ro, labels)
            fw_ro.write(
                str(i)+'prep, recall, acc, f1:' + '\t' + prep_ro + '\t' + recall_ro + '\t' + acc_ro + '\t' + f1_ro + '\n')

            pre_avg = getpre(i, s_avg)
            prep_avg, recall_avg, acc_avg, f1_avg = eval(pre_avg, labels)
            fw_avg.write(
                str(i) +str(i)+ 'prep, recall, acc, f1:' + '\t' + prep_avg + '\t' + recall_avg + '\t' + acc_avg + '\t' + f1_avg + '\n')

            pre_f = getpre(i, s_f)
            prep_f, recall_f, acc_f, f1_f = eval(pre_f, labels)
            fw_f.write(str(i)+'prep, recall, acc, f1:' + '\t' + prep_f + '\t' + recall_f + '\t' + acc_f + '\t' + f1_f + '\n')
            i += 0.01
