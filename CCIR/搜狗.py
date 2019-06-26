# encoding:utf-8
# 输入序列长度
n = input()
flag_list = ['*',';','[',']','(',')',',']
sign_list = []
right_list = [']',')']
num_list = []
for str in n:
    if str in flag_list:
        if str not in right_list:
            sign_list.append(str)
        else:
            # 弹出
            
    else:
        num = int(str)
        num_list.append(num)


    print(int(str))
