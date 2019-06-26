# encoding:utf-8

# n 礼品总数
n = int(input())
# m表示礼品价格
m = input()
# p 表示价格
p = int(input())
Price = []
for i in m.split(" "):
    Price.append(int(i))
Price = sorted(Price)
index = n
flag = 0
for j in range(0, n+1):
    if p == 0:
        flag = 1
    else:
        if Price[index-1] <= p:
            p = p - Price[index-1]
            index = index - 1
        else:
            index = index - 1
            continue
if flag == 1:
    print('1')

