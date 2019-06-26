# encoding:utf-8


def fun(a, k):
    # 输入list
    # a = [4, 6]
    # 操作次数k
    # k = 2
    flag = True
    for i in range(k):
        for j in range(len(a)):
            if flag and a[j] != 0:
                temp = a[0]
                flag = False
            elif a[j] < temp and a[j] != 0:
                temp = a[j]
        print(temp)
        for k in range(len(a)):
            a[k] = a[k] - temp


a = [5, -4, 1, -3, 1]
total_cost = 0
for i in range(len(a)):
    if a[i] < 0 and i-1 != -1 and i+1 != len(a):
        if a[i+1] > 0 and a[i+1] > a[i]:
            a[i+1] = a[i+1] - a[i]
            total_cost += a[i]
            a[i] = 0
        elif a[i-1] > 0 and a[i-1] > a[i]:
            a[i-1] = a[i-1] - a[i]
            total_cost += a[i]
            a[i] = 0
print(-total_cost)


