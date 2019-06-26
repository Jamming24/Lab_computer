def scane(x, file):
    for _ in x:
        if islist(_):
            file.writelines('\n')
            scane(_, file)
        else:
            file.writelines(str(type(_)).replace('<class \'', "").replace('\'>', '') + ':' + str(_) + '\t')


def islist(x):
    bool = False
    if type(x) == list:
        bool = True
    return bool


def write(a, path):
    with open(path, 'w', encoding="utf-8") as file:
        scane(a, file)
        print('写入完成。。。')


def read(path):
    result = []
    with open(path, 'r', encoding="utf-8") as file2:
        l1 = list(file2)
        print(l1)
        len1 = len(l1)
        print(l1)
        print('len1:', len1)
        i = len1 - 1
        print(i)
        while (i >= 0):
            if i == len1 - 1:
                temp = []
                line = l1[i].replace('\n', '')
                list1 = line.split('\t')
                for _ in list1:
                    l2 = _.split(':')
                    # print(l2[0],l2[1])
                    if l2[0] + '1' == 'str1':
                        temp.append(str(l2[1]))
                    elif l2[0] + '1' == 'int1':
                        temp.append(int(l2[1]))
                    elif l2[0] + '1' == 'float1':
                        temp.append(float(l2[1]))

                result = temp
                print(result)
            else:
                temp = []
                line = l1[i]
                list1 = line.split('\t')
                for _ in list1:
                    l2 = _.split(':')
                    if l2[0] + '1' == 'str1':
                        temp.append(str(l2[1]))
                    elif l2[0] + '1' == 'int1':
                        temp.append(int(l2[1]))
                    elif l2[0] + '1' == 'float1':
                        temp.append(float(l2[1]))
                temp.append(result)
                result = temp
                print(result)
            i -= 1
    print(result)


# a = [12, "abc", [0.4, ["bcd"],['good',1354,46454]]]
# path = '..\seqgan\demo.txt'
# # 写文件
# write(a,path)
# # 读文件
# read(path)



#  _____________________________________________________________________________
# import nltk
# s = 'This is a cats.'
# text = nltk.word_tokenize(s.lower())
# [word_index_dict, index_word_dict] = get_dict(text)
# print(text)


def twoSum(nums, target):  # 56ms
    result = []
    map1 = {}
    for x in range(len(nums)):
        temp = target - nums[x]
        if nums[x] in map1.keys() and map1.get(temp) != x:
            result.extend([map1.get(nums[x]), x])
            break
        map1.setdefault(temp, x)
    return result

def twoSum2(nums,target):  #48ms
    alist = {}
    for x, y in enumerate(nums):
        if y in alist:
            z = alist[y]
            return [z,x]
        alist[target-y] = x
    return None
# nums = [2, 2, 7, 11, 15]
# # print(nums.index(2))
# target = 4
# print(twoSum(nums, target))


import tensorflow as tf
l1 = tf.constant(0.5)
l2 = tf.constant(1.0)
result = l1+l2

# with tf.Session() as sess:
#     print(sess.run(result))
import numpy as np
lll = [[0,1],[0,1]]
aaa = [[1,0],[1,0]]
# la = np.concatenate([lll,aaa],0)
# print(la[1,2,3,0])
for l,a in zip(lll,aaa):
    print("l,a: ",l,a)


# lll = [0,1,2,3,4,5]
# lll = np.array(lll)
# shuffle_indices = np.random.permutation(np.arange(6))
# lll_shuff = lll[shuffle_indices]
# print(lll_shuff)
# print(np.split(lll_shuff,2,0))




